# FastAPI URL Shortener

A simple URL shortener built with FastAPI.

## 📦 Running with Docker

1. **Build the Docker image:**
   ```sh
   docker build -t fastapi-app .
   ```

2. **Run the container:**
   ```sh
   docker run -p 8080:8080 fastapi-app
   ```

or using `docker-compose`:

```sh
   docker-compose up --build -d
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/shorten` | Shorten a URL |
| `GET` | `/{short_id}` | Redirect to original URL |
| `GET` | `/external-api/` | Fetch data from external API |

## 🏋 Load Testing
Load testing was performed to assess performance.

### Running Load Tests

To run load tests, execute:
```sh
locust -f locustfile.py --host=http://127.0.0.1:8080
```
Then, open the Locust web interface at:
```
http://localhost:8089/
```

Example test configuration:

- **Number of users (peak concurrency):** 50
- **Ramp-up (users started per second):** 50
- **Host:** `http://127.0.0.1:8080`

Results:

| Type | Name | # Requests | # Fails | Median (ms) | 95%ile (ms) | 99%ile (ms) | Average (ms) | Min (ms) | Max (ms) | Avg Size (bytes) | RPS | Failures/s |
|------|------|------------|--------|------------|------------|------------|------------|--------|--------|----------------|----|-------------|
| `GET` | `/external-api/` | 5499 | 0 | 730 | 1300 | 1700 | 790.43 | 375 | 2086 | 66 | 7.3 | 0 |
| `POST` | `/shorten` | 10870 | 0 | 110 | 700 | 1100 | 200.4 | 8 | 1629 | 46 | 13.2 | 0 |
| **Aggregated** | | 16369 | 0 | 290 | 1100 | 1500 | 398.62 | 8 | 2086 | 52.72 | 20.5 | 0 |

## 📜 License
MIT License

