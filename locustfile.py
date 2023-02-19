from locust import HttpUser, task


class getprime(HttpUser):
    @task
    def getprime(self):
        self.client.get("lp/12")

    @task(2)
    def getprime(self):
        self.client.get("lp/10000009")

    @task(3)
    def getprime(self):
        self.client.get("time")