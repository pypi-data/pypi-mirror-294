import time
from functools import lru_cache, wraps
from urllib.parse import urlparse

from mlflow.utils.rest_utils import MlflowHostCreds, http_request_safe

from mlfoundry.exceptions import MlFoundryException
from mlfoundry.run_utils import append_servicefoundry_path_to_tracking_ui
from mlfoundry.tracking.entities import PythonSDKConfig, TenantInfo, Token


def timed_lru_cache(seconds: int = 300, maxsize: int = None):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.delta = seconds * 10**9
        func.expiration = time.monotonic_ns() + func.delta

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.monotonic_ns() >= func.expiration:
                func.cache_clear()
                func.expiration = time.monotonic_ns() + func.delta
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@timed_lru_cache(seconds=30 * 60)
def _cached_get_python_sdk_config(host: str) -> PythonSDKConfig:
    host_creds = MlflowHostCreds(host=host)
    response = http_request_safe(
        host_creds=host_creds,
        endpoint="/v1/min-cli-version",
        method="get",
        timeout=3,
        max_retries=2,
    )
    response = response.json()
    return PythonSDKConfig.parse_obj(response)


@timed_lru_cache(seconds=30 * 60)
def _cached_get_tenant_info(host: str) -> TenantInfo:
    host_creds = MlflowHostCreds(host=host)
    response = http_request_safe(
        host_creds=host_creds,
        endpoint="/v1/tenant-id",
        params={"hostName": urlparse(host).netloc},
        method="get",
        timeout=3,
        max_retries=2,
    )
    response = response.json()
    return TenantInfo.parse_obj(response)


class ServicefoundryService:
    def __init__(self, tracking_uri: str, token: str = None):
        self.host_creds = MlflowHostCreds(
            host=append_servicefoundry_path_to_tracking_ui(tracking_uri), token=token
        )

    @property
    def python_sdk_config(self) -> PythonSDKConfig:
        return _cached_get_python_sdk_config(
            host=self.host_creds.host,
        )

    @property
    def tenant_info(self) -> TenantInfo:
        return _cached_get_tenant_info(
            host=self.host_creds.host,
        )

    def get_token_from_api_key(self, api_key: str) -> Token:
        response = http_request_safe(
            host_creds=self.host_creds,
            endpoint="/v1/oauth/api-key/token",
            method="get",
            params={"apiKey": api_key},
            timeout=3,
            max_retries=2,
        )
        response = response.json()
        return Token.parse_obj(response)

    def get_integration_from_id(self, integration_id: str):
        integration_id = integration_id or ""
        try:
            response = http_request_safe(
                host_creds=self.host_creds,
                endpoint=f"/v1/provider-accounts/provider-integrations",
                params={"id": integration_id, "type": "blob-storage"},
                method="get",
                timeout=3,
                max_retries=1,
            )
            data = response.json()
            if (
                data.get("providerIntegrations")
                and len(data["providerIntegrations"]) > 0
                and data["providerIntegrations"][0]
            ):
                return data["providerIntegrations"][0]
            else:
                raise MlFoundryException(
                    f"Invalid storage integration id: {integration_id}"
                )
        except MlFoundryException:
            raise
        except Exception:
            response = http_request_safe(
                host_creds=self.host_creds,
                endpoint=f"/v1/integrations/{integration_id}",
                method="get",
                timeout=3,
                max_retries=1,
            )
            return response.json()
