import time
from abc import ABC, abstractmethod

import requests

from truefoundry.deploy.lib.clients.utils import poll_for_function, request_handling
from truefoundry.deploy.lib.const import VERSION_PREFIX
from truefoundry.deploy.lib.exceptions import BadRequestException
from truefoundry.deploy.lib.model.entity import DeviceCode, Token
from truefoundry.logger import logger


class AuthServiceClient(ABC):
    def __init__(self, base_url):
        from truefoundry.deploy.lib.clients.servicefoundry_client import (
            ServiceFoundryServiceClient,
        )

        client = ServiceFoundryServiceClient(init_session=False, base_url=base_url)

        self._api_server_url = client._api_server_url
        self._auth_server_url = client.tenant_info.auth_server_url
        self._tenant_name = client.tenant_info.tenant_name

    @classmethod
    def from_base_url(cls, base_url: str) -> "AuthServiceClient":
        from truefoundry.deploy.lib.clients.servicefoundry_client import (
            ServiceFoundryServiceClient,
        )

        client = ServiceFoundryServiceClient(init_session=False, base_url=base_url)
        if client.python_sdk_config.use_sfy_server_auth_apis:
            return ServiceFoundryServerAuthServiceClient(base_url)
        return AuthServerServiceClient(base_url)

    @abstractmethod
    def refresh_token(self, token: Token, host: str = None) -> Token: ...

    @abstractmethod
    def get_device_code(self) -> DeviceCode: ...

    @abstractmethod
    def get_token_from_device_code(
        self, device_code: str, timeout: float = 60, poll_interval_seconds: int = 1
    ) -> Token: ...


class ServiceFoundryServerAuthServiceClient(AuthServiceClient):
    def __init__(self, base_url):
        super().__init__(base_url)

    def refresh_token(self, token: Token, host: str = None) -> Token:
        host_arg_str = f"--host {host}" if host else "--host HOST"
        if not token.refresh_token:
            # TODO: Add a way to propagate error messages without traceback to the output interface side
            raise Exception(
                f"Unable to resume login session. Please log in again using `tfy login {host_arg_str} --relogin`"
            )
        url = f"{self._api_server_url}/{VERSION_PREFIX}/oauth2/token"
        data = {
            "tenantName": token.tenant_name,
            "refreshToken": token.refresh_token,
            "grantType": "refresh_token",
            "returnJWT": True,
        }
        res = requests.post(url, json=data)
        try:
            res = request_handling(res)
            return Token.parse_obj(res)
        except BadRequestException as ex:
            raise Exception(
                f"Unable to resume login session. Please log in again using `tfy login {host_arg_str} --relogin`"
            ) from ex

    def get_device_code(self) -> DeviceCode:
        url = f"{self._api_server_url}/{VERSION_PREFIX}/oauth2/device-authorize"
        data = {"tenantName": self._tenant_name}
        res = requests.post(url, json=data)
        res = request_handling(res)
        return DeviceCode.parse_obj(res)

    def get_token_from_device_code(
        self, device_code: str, timeout: float = 60, poll_interval_seconds: int = 1
    ) -> Token:
        timeout = timeout or 60
        poll_interval_seconds = poll_interval_seconds or 1
        url = f"{self._api_server_url}/{VERSION_PREFIX}/oauth2/token"
        data = {
            "tenantName": self._tenant_name,
            "deviceCode": device_code,
            "grantType": "device_code",
            "returnJWT": True,
        }
        response = requests.post(url=url, json=data)
        start_time = time.monotonic()

        for response in poll_for_function(
            requests.post, poll_after_secs=poll_interval_seconds, url=url, json=data
        ):
            if response.status_code == 201:
                response = response.json()
                return Token.parse_obj(response)
            elif response.status_code == 202:
                logger.debug("User has not authorized yet. Checking again.")
            else:
                raise Exception(
                    "Failed to get token using device code. "
                    f"status_code {response.status_code},\n {response.text}"
                )
            time_elapsed = time.monotonic() - start_time
            if time_elapsed > timeout:
                logger.warning("Polled server for %s secs.", int(time_elapsed))
                break

        raise Exception(f"Did not get authorized within {timeout} seconds.")


class AuthServerServiceClient(AuthServiceClient):
    def __init__(self, base_url):
        super().__init__(base_url)

    def refresh_token(self, token: Token, host: str = None) -> Token:
        host_arg_str = f"--host {host}" if host else "--host HOST"
        if not token.refresh_token:
            # TODO: Add a way to propagate error messages without traceback to the output interface side
            raise Exception(
                f"Unable to resume login session. Please log in again using `tfy login {host_arg_str} --relogin`"
            )
        url = f"{self._auth_server_url}/api/{VERSION_PREFIX}/oauth/token/refresh"
        data = {
            "tenantName": token.tenant_name,
            "refreshToken": token.refresh_token,
        }
        res = requests.post(url, json=data)
        try:
            res = request_handling(res)
            return Token.parse_obj(res)
        except BadRequestException as ex:
            raise Exception(
                f"Unable to resume login session. Please log in again using `tfy login {host_arg_str} --relogin`"
            ) from ex

    def get_device_code(self) -> DeviceCode:
        url = f"{self._auth_server_url}/api/{VERSION_PREFIX}/oauth/device"
        data = {"tenantName": self._tenant_name}
        res = requests.post(url, json=data)
        res = request_handling(res)
        # TODO: temporary cleanup of incorrect attributes
        res = {"userCode": res.get("userCode"), "deviceCode": res.get("deviceCode")}
        return DeviceCode.parse_obj(res)

    def get_token_from_device_code(
        self, device_code: str, timeout: float = 60, poll_interval_seconds: int = 1
    ) -> Token:
        url = f"{self._auth_server_url}/api/{VERSION_PREFIX}/oauth/device/token"
        data = {
            "tenantName": self._tenant_name,
            "deviceCode": device_code,
        }
        start_time = time.monotonic()
        poll_interval_seconds = 1

        for response in poll_for_function(
            requests.post, poll_after_secs=poll_interval_seconds, url=url, json=data
        ):
            if response.status_code == 201:
                response = response.json()
                return Token.parse_obj(response)
            elif response.status_code == 202:
                logger.debug("User has not authorized yet. Checking again.")
            else:
                raise Exception(
                    "Failed to get token using device code. "
                    f"status_code {response.status_code},\n {response.text}"
                )
            time_elapsed = time.monotonic() - start_time
            if time_elapsed > timeout:
                logger.warning("Polled server for %s secs.", int(time_elapsed))
                break

        raise Exception(f"Did not get authorized within {timeout} seconds.")
