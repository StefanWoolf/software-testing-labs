import uuid

from locust import HttpUser, SequentialTaskSet, between, task


class CreateAndReadPost(SequentialTaskSet):
    @task
    def create_post(self):
        with self.client.post(
            "/posts",
            json={"author": self.user.username, "title": "Load test", "content": "Hello"},
            catch_response=True,
        ) as resp:
            if resp.status_code != 201:
                resp.failure(f"status {resp.status_code}")
                self.interrupt()
            self.post_id = resp.json()["id"]

    @task
    def read_created_post(self):
        self.client.get(f"/posts/{self.post_id}", name="/posts/[id]")
        self.interrupt()


def read_all_posts(user):
    user.client.get("/posts")


def read_first_post(user):
    user.client.get("/posts/1")


class BlogUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 2)
    tasks = {CreateAndReadPost: 1, read_all_posts: 5, read_first_post: 3}

    def on_start(self):
        self.username = f"user_{uuid.uuid4()}"
