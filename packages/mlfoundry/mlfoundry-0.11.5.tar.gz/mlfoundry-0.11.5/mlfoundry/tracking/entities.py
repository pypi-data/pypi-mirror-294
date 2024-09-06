import enum
import time
from typing import Dict, Optional

import jwt

from mlfoundry.pydantic_v1 import BaseModel, Field, constr, validator


class TenantInfo(BaseModel):
    tenant_name: constr(min_length=1) = Field(alias="tenantName")
    auth_server_url: str

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False


class ArtifactCredential(BaseModel):
    run_id: str
    path: str
    signed_uri: str


class UserType(enum.Enum):
    user = "user"
    serviceaccount = "serviceaccount"


class UserInfo(BaseModel):
    user_id: constr(min_length=1)
    user_type: UserType = UserType.user
    email: Optional[str] = None
    tenant_name: constr(min_length=1) = Field(alias="tenantName")

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False


class Token(BaseModel):
    access_token: constr(min_length=1) = Field(alias="accessToken", repr=False)
    refresh_token: Optional[constr(min_length=1)] = Field(
        alias="refreshToken", repr=False
    )
    decoded_value: Optional[Dict] = Field(exclude=True, repr=False)

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    @validator("decoded_value", always=True, pre=True)
    def _decode_jwt(cls, v, values, **kwargs):
        access_token = values["access_token"]
        return jwt.decode(
            access_token,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_exp": False,
            },
        )

    @property
    def tenant_name(self) -> str:
        return self.decoded_value["tenantName"]

    def is_going_to_be_expired(self, buffer_in_seconds: int = 120) -> bool:
        exp = int(self.decoded_value["exp"])
        return (exp - time.time()) < buffer_in_seconds

    def to_user_info(self) -> UserInfo:
        return UserInfo(
            user_id=self.decoded_value["username"],
            email=self.decoded_value["email"]
            if "email" in self.decoded_value
            else None,
            user_type=UserType(self.decoded_value.get("userType", UserType.user.value)),
            tenant_name=self.tenant_name,
        )


class DeviceCode(BaseModel):
    user_code: str = Field(alias="userCode")
    device_code: str = Field(alias="deviceCode")
    verification_url: Optional[str] = Field(alias="verificationURI")
    complete_verification_url: Optional[str] = Field(alias="verificationURIComplete")
    expires_in_seconds: int = Field(alias="expiresInSeconds", default=60)
    interval_in_seconds: int = Field(alias="intervalInSeconds", default=1)
    message: Optional[str] = Field(alias="message")

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    def get_user_clickable_url(self, tracking_uri: str) -> str:
        return f"{tracking_uri}/authorize/device?userCode={self.user_code}"


class PythonSDKConfig(BaseModel):
    min_version: str = Field(alias="minVersion")
    truefoundry_cli_min_version: str = Field(alias="truefoundryCliMinVersion")
    use_sfy_server_auth_apis: Optional[bool] = Field(
        alias="useSFYServerAuthAPIs", default=False
    )

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False
