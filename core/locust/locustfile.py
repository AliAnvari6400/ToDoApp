from locust import HttpUser, task


class task_list(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            data={"email": "a_anvari@ymail.com", "password": "anvari@7768"},
        ).json()

        self.client.headers.update(
            {"Authorization": f"Bearer {response.get('access',None)}"}
        )

    @task
    def task(self):
        self.client.get("/todo/api/v1/task/")
