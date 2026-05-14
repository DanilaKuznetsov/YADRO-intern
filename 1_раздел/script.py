from __future__ import annotations

import http.client
import logging
from dataclasses import dataclass
from urllib.parse import urlparse


BASE_URL = "https://httpstat.us"
REQUEST_STATUSES = (102, 200, 301, 404, 500)
TIMEOUT_SECONDS = 10


class HttpStatusError(Exception):
    pass


@dataclass(frozen=True)
class HttpResponse:
    url: str
    status_code: int
    body: str


def request_status(status_code: int) -> HttpResponse:
    url = f"{BASE_URL}/{status_code}"
    parsed_url = urlparse(url)

    connection = http.client.HTTPSConnection(parsed_url.netloc, timeout=TIMEOUT_SECONDS)
    try:
        connection.request(
            "GET",
            parsed_url.path,
            headers={
                "Accept": "text/plain",
                "Connection": "close",
                "User-Agent": "yadro-intern-status-checker/1.0",
            },
        )
        response = connection.getresponse()
        body = response.read().decode("utf-8", errors="replace")
        return HttpResponse(url=url, status_code=response.status, body=body)
    finally:
        connection.close()


def handle_response(response: HttpResponse) -> None:
    if 100 <= response.status_code < 400:
        logging.info("Response from %s", response.url)
        logging.info("Status code: %s", response.status_code)
        logging.info("Body: %s", response.body or "<empty>")
        return

    if 400 <= response.status_code < 600:
        raise HttpStatusError(
            f"{response.url} returned {response.status_code}: {response.body or '<empty>'}"
        )

    raise ValueError(f"Unsupported HTTP status code: {response.status_code}")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    for status_code in REQUEST_STATUSES:
        logging.info("Requesting status %s", status_code)
        try:
            response = request_status(status_code)
            handle_response(response)
        except HttpStatusError as error:
            logging.exception("HTTP exception was handled: %s", error)
        except OSError as error:
            logging.exception("Network error while requesting %s: %s", status_code, error)
        logging.info("-" * 60)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
