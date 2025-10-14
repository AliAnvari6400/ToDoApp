from locust import HttpUser, task


class task_list(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/todo/api/v1/task/")
