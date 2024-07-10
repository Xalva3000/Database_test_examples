import requests


class CustomResponse:
    def __init__(self, path):
        self.path = path
        self.response = self.get_response()

    def get_response(self):
        response = requests.get(self.path, timeout=3)
        return response

    def get_response_headers(self):
        return self.response.headers

    def get_response_status(self):
        return self.response.status_code

    def get_cookies(self):
        return self.response.cookies

    def get_authentication(self, username, password):
        login_path = f"{self.path}/basic-auth/{username}/{password}"
        response = requests.get(login_path, auth=(username, password))
        return response


def internet(username, password):
    path = "https://httpbin.org"
    cr = CustomResponse(path)
    proxy = {'https': 'localhost:8082'}
    requests.get("https://ya.ru", proxies=proxy, verify=False)


if __name__ == "__main__":
    internet('alex', '12345')
