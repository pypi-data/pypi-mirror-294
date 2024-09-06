from typing import Any

import httpx
from httpx import USE_CLIENT_DEFAULT, Response, Request
from httpx._types import AuthTypes
from openai import OpenAI
from openai import _constants as oai_constants


def auth_interceptor(key: str, secret: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Authenticating with key: {key}, secret: {secret}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


class CustomHttpxClient(httpx.Client):

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("timeout", oai_constants.DEFAULT_TIMEOUT)
        kwargs.setdefault("limits", oai_constants.DEFAULT_CONNECTION_LIMITS)
        kwargs.setdefault("follow_redirects", True)
        super().__init__(**kwargs)

    @auth_interceptor("test_key", "test_secret")
    def send(
            self,
            request: Request,
            *,
            stream: bool = False,
            auth: AuthTypes | None = USE_CLIENT_DEFAULT,
            follow_redirects: bool = True,
    ) -> Response:
        return super().send(request, stream=stream, auth=auth, follow_redirects=follow_redirects)


if __name__ == "__main__":
    client = OpenAI(
        api_key='<KEY>',
        base_url="http://127.0.0.1:8000/v1",
        http_client=CustomHttpxClient(),
    )
    response = client.chat.completions.create(
        model="custom_model",
        messages=[{"role": "user", "content": "what's your name?"}],
    )
    print(response.choices[0].message.content)
