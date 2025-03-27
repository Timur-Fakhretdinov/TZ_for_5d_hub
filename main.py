from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import shortuuid
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
import httpx
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# Настройка БД
DATABASE_URL = "sqlite:///./shortener.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URLModel(Base):
    __tablename__ = "urls"
    short_id = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic модель запроса
class URLRequest(BaseModel):
    url: HttpUrl

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/shorten", status_code=201)
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    short_id = shortuuid.uuid()[:8]
    db_url = URLModel(short_id=short_id, original_url=str(request.url))
    db.add(db_url)
    db.commit()
    return {"short_url": f"http://127.0.0.1:8080/{short_id}"}

@app.get("/{short_id}")
def redirect_to_url(short_id: str, db: Session = Depends(get_db)):
    db_url = db.query(URLModel).filter(URLModel.short_id == short_id).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=db_url.original_url, status_code=307)

@app.get("/external-api/")
async def fetch_external_data():
    url = "https://jsonplaceholder.typicode.com/todos/1"  # Пример API
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
