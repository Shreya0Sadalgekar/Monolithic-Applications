from locust import task, run_single_user, FastHttpUser
from insert_product import login


class AddToCartUser(FastHttpUser):
    host = "http://localhost:5000"

    def __init__(self, environment):
        super().__init__(environment)
        self.username = "test123"
        self.password = "test123"
        self.token = None
        self.default_headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        }

    def on_start(self):
        # Login and retrieve the token
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")

    @task
    def add_to_cart(self):
        if not self.token:
            self.environment.runner.quit()
            print("Token not found, stopping the test!")
            return

        with self.client.get(
            "/cart",
            headers={
                **self.default_headers,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,/;q=0.8",
                "Referer": "http://localhost:5000/product/1",
                "Upgrade-Insecure-Requests": "1",
            },
            cookies={"token": self.token},
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")


if __name__ == "__main__":
    run_single_user(AddToCartUser)

