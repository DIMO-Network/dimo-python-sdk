from dimo.errors import check_type


class User:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def user(self, access_token: str) -> dict:
        check_type("access_token", access_token, str)
        return self._request(
            "GET", "User", "/v1/user", headers=self._get_auth_headers(access_token)
        )

    def update_user(self, access_token: str, user_update_request: dict) -> dict:
        check_type("access_token", access_token, str)
        check_type("update_user_request", user_update_request, dict)
        body = {"userUpdateRequest": user_update_request}
        return self._request(
            "PUT",
            "User",
            "/v1/user",
            data=body,
            headers=self._get_auth_headers(access_token),
        )

    def delete_user(self, access_token: str) -> None:
        check_type("access_token", access_token, str)
        return self._request(
            "DELETE", "User", "/v1/user", headers=self._get_auth_headers(access_token)
        )

    def send_confirmation_email(self, access_token: str) -> None:
        check_type("access_token", access_token, str)
        return self._request(
            "POST",
            "User",
            "/v1/user/send-confirmation-email",
            headers=self._get_auth_headers(access_token),
        )

    def confirm_email(self, access_token: str, confirm_email_request: dict) -> None:
        check_type("access_token", access_token, str)
        check_type("confirm_email_request", confirm_email_request, dict)
        body = {"confirmEmailRequest": confirm_email_request}
        return self._request(
            "POST",
            "User",
            "/v1/user/confirm-email",
            data=body,
            headers=self._get_auth_headers(access_token),
        )
