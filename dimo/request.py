import json
from requests import Session, RequestException
from .errors import HTTPError


class Request:

    def __init__(self, http_method: str, url: str, session: Session):
        self.http_method = http_method
        self.url = url
        self.session = session

    def __call__(self, headers=None, data=None, params=None, **kwargs):
        headers = headers or {}
        headers.update(kwargs.pop("headers", {}))

        if (
            data
            and isinstance(data, dict)
            and headers.get("Content-Type") == "application/json"
        ):
            data = json.dumps(data)

        try:
            response = self.session.request(
                method=self.http_method,
                url=self.url,
                headers=headers,
                params=params,
                data=data,
                **kwargs,
            )

            response.raise_for_status()
        except RequestException as exc:
            status = getattr(exc.response, "status_code", None)
            body = None
            try:
                body = exc.response.json()
            except Exception:
                body = exc.response.txt if exc.response else None
            raise HTTPError(status=status or -1, message=str(exc), body=body)

        content_type = response.headers.get("Content-Type", "")
        if "json" in content_type:
            return response.json()

        return response.content
