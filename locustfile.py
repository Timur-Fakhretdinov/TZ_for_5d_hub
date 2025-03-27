from locust import HttpUser, task, between

class LoadTest(HttpUser):
    wait_time = between(1, 3)  # Интервал между запросами (1-3 сек)

    @task(2)  # Делаем `POST` в 2 раза чаще, чем `GET`
    def shorten_url(self):
        self.client.post("/shorten", json={"url": "https://example.com"})

    @task(1)  # Читаем случайные ссылки
    def redirect_url(self):
        self.client.get("/external-api/")  # Запрос к внешнему API
