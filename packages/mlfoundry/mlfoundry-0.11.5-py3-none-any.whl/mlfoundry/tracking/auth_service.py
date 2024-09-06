import time
from abc import ABC, abstractmethod
from typing import Any, Callable, Generator

import requests
from mlflow.utils.rest_utils import MlflowHostCreds, http_request, http_request_safe

from mlfoundry.exceptions import MlFoundryException
from mlfoundry.logger import logger
from mlfoundry.tracking.entities import DeviceCode, Token


def poll_for_function(
    func: Callable, poll_after_secs: int = 5, *args, **kwargs
) -> Generator[Any, None, None]:
    while True:
        yield func(*args, **kwargs)
        time.sleep(poll_after_secs)


class AuthServiceClient(ABC):
    def __init__(self, base_url):
        from mlfoundry.tracking.servicefoundry_service import ServicefoundryService

        client = ServicefoundryService(tracking_uri=base_url, token=None)
        self._api_server_url = client.host_creds.host
        self._auth_server_url = client.tenant_info.auth_server_url
        self._tenant_name = client.tenant_info.tenant_name

    @classmethod
    def from_base_url(cls, base_url: str) -> "AuthServiceClient":
        from mlfoundry.tracking.servicefoundry_service import ServicefoundryService

        client = ServicefoundryService(tracking_uri=base_url, token=None)
        if client.python_sdk_config.use_sfy_server_auth_apis:
            return ServiceFoundryServerAuthServiceClient(base_url)
        return AuthServerServiceClient(base_url)

    @abstractmethod
    def refresh_token(self, token: Token, host: str = None) -> Token:
        ...

    @abstractmethod
    def get_device_code(self) -> DeviceCode:
        ...

    @abstractmethod
    def get_token_from_device_code(
        self, device_code: str, timeout: float = 60, poll_interval_seconds: int = 1
    ) -> Token:
        ...


class ServiceFoundryServerAuthServiceClient(AuthServiceClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.host_creds = MlflowHostCreds(host=self._api_server_url)

    def refresh_token(self, token: Token, host: str = None) -> Token:
        host_arg_str = f"--host {host}" if host else "--host HOST"
        if not token.refresh_token:
            # TODO: Add a way to propagate error messages without traceback to the output interface side
            raise MlFoundryException(
                f"Unable to resume login session. Please log in again using `tfy login {host_arg_str} --relogin`"
            )
        try:
            response = http_request(
                host_creds=self.host_creds,
                endpoint="/v1/oauth2/token",
                method="post",
                json={
                    "tenantName": token.tenant_name,
                    "refreshToken": token.refresh_token,
                    "grantType": "refresh_token",
                    "returnJWT": True,
                },
                timeout=3,
                max_retries=1,
            )
            response.raise_for_status()
            return Token.parse_obj(response.json())
        except requests.exceptions.HTTPError as he:
            if 400 <= he.response.status_code < 500:
                raise MlFoundryException(
                    f"Unable to resume login session. Please log in again using `tfy login {host_arg_str} --relogin`"
                )
            raise MlFoundryException(
                f"Unable to resume login session. Something went wrong"
            ) from he
        except Exception as ex:
            raise MlFoundryException(f"Unable to resume login session.") from ex

    def get_device_code(self) -> DeviceCode:
        response = http_request_safe(
            host_creds=self.host_creds,
            endpoint="/v1/oauth2/device-authorize",
            method="post",
            json={"tenantName": self._tenant_name},
            timeout=3,
            max_retries=0,
        )
        response = response.json()
        return DeviceCode.parse_obj(response)

    def get_token_from_device_code(
        self, device_code: str, timeout: float = 60, poll_interval_seconds: int = 1
    ) -> Token:
        timeout = timeout or 60
        poll_interval_seconds = poll_interval_seconds or 1
        data = {
            "tenantName": self._tenant_name,
            "deviceCode": device_code,
            "grantType": "device_code",
            "returnJWT": True,
        }
        start_time = time.monotonic()
        for response in poll_for_function(
            http_request,
            poll_after_secs=poll_interval_seconds,
            host_creds=self.host_creds,
            endpoint="/v1/oauth2/token",
            method="post",
            json=data,
            timeout=3,
            max_retries=0,
        ):
            if response.status_code == 201:
                response = response.json()
                return Token.parse_obj(response)
            elif response.status_code == 202:
                logger.debug("User has not authorized yet. Checking again.")
            else:
                raise MlFoundryException(
                    "Failed to get token using device code. "
                    f"status_code {response.status_code},\n {response.text}"
                )
            time_elapsed = time.monotonic() - start_time
            if time_elapsed > timeout:
                logger.warning("Polled server for %s secs.", int(time_elapsed))
                break

        raise MlFoundryException(f"Did not get authorized within {timeout} seconds.")


class AuthServerServiceClient(AuthServiceClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.host_creds = MlflowHostCreds(host=self._auth_server_url)

    def refresh_token(self, token: Token, host: str = None) -> Token:
        host_arg_str = f"--host {host}" if host else "--host HOST"
        if not token.refresh_token:
            # TODO: Add a way to propagate error messages without traceback to the output interface side
            raise MlFoundryException(
                f"Unable to resume login session. Please log in again using `tfy login {host_arg_str} --relogin`"
            )
        try:
            response = http_request(
                host_creds=self.host_creds,
                endpoint="/api/v1/oauth/token/refresh",
                method="post",
                json={
                    "tenantName": token.tenant_name,
                    "refreshToken": token.refresh_token,
                },
                timeout=3,
                max_retries=0,
            )
            response = response.json()
            return Token.parse_obj(response)
        except requests.exceptions.HTTPError as he:
            if 400 <= he.response.status_code < 500:
                raise MlFoundryException(
                    f"Unable to resume login session. Please log in again using `tfy login {host_arg_str} --relogin`"
                )
            raise MlFoundryException(
                f"Unable to resume login session. Something went wrong"
            ) from he
        except Exception as ex:
            raise MlFoundryException(f"Unable to resume login session.") from ex

    def get_device_code(self) -> DeviceCode:
        response = http_request_safe(
            host_creds=self.host_creds,
            endpoint="/api/v1/oauth/device",
            method="post",
            json={"tenantName": self._tenant_name},
            timeout=3,
            max_retries=0,
        )
        response = response.json()
        return DeviceCode.parse_obj(response)

    def get_token_from_device_code(
        self, device_code: str, timeout: float = 60, poll_interval_seconds: int = 1
    ) -> Token:
        data = {
            "tenantName": self._tenant_name,
            "deviceCode": device_code,
        }
        start_time = time.monotonic()
        poll_interval_seconds = 1

        for response in poll_for_function(
            http_request,
            poll_after_secs=poll_interval_seconds,
            host_creds=self.host_creds,
            endpoint="/api/v1/oauth/device/token",
            method="post",
            json=data,
            timeout=3,
            max_retries=0,
        ):
            if response.status_code == 201:
                response = response.json()
                return Token.parse_obj(response)
            elif response.status_code == 202:
                logger.debug("User has not authorized yet. Checking again.")
            else:
                raise MlFoundryException(
                    "Failed to get token using device code. "
                    f"status_code {response.status_code},\n {response.text}"
                )
            time_elapsed = time.monotonic() - start_time
            if time_elapsed > timeout:
                logger.warning("Polled server for %s secs.", int(time_elapsed))
                break

        raise MlFoundryException(f"Did not get authorized within {timeout} seconds.")
