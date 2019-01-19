import random
import time

import requests
from requests import ConnectionError

import sample_backend

URL = "http://localhost:8080/publish/"


def publish(content):
    r = requests.post(URL, {
        'content': content,
    })
    r.raise_for_status()
    return r.status_code


def main():
    while True:
        s = sample_backend.foo()
        print(s)
        try:
            code = publish(s)
            print(">", code)
        except ConnectionError as e:
            print("!", e)

        time.sleep(random.uniform(1, 4))


if __name__ == "__main__":
    main()
