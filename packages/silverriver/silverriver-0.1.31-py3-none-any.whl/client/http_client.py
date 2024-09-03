import json
import sys
from typing import TypeVar

import httpx
import pydantic

from silverriver.client.agent_endpoints import SotaAgentEndpoints
from silverriver.client.browser_endpoints import BrowserEndpoints
from silverriver.interfaces import Observation, AgentAction, SetupOutput, SubTransition, SetupInput
from silverriver.utils.remote_browser import connect_to_remote_session

T = TypeVar('T', bound=pydantic.BaseModel)
API_HOST = "crux.silverstream.ai"
API_PORT = 31337
API_SERVER_URL = f"http://{API_HOST}:{API_PORT}"
DEBUG = sys.gettrace() is not None


class HTTPCruxClient(httpx.Client):
    def __init__(self, api_key: str, base_url: str = API_SERVER_URL, **kwargs):
        if DEBUG:
            kwargs.setdefault('timeout', 30_000.0)
        else:
            kwargs.setdefault('timeout', 30.0)

        headers = {"X-API-Key": api_key}
        super().__init__(base_url=base_url, headers=headers, **kwargs)

        # Fail early if not connected
        try:
            # 404 is expected, we just want to check if the server is up
            self.request("GET", "/version")
        except httpx.ConnectError:
            raise httpx.ConnectError("The server might not be up")

    # TODO: make_request should use the Endpoint model directly rather than unpacking it
    def _make_request(self, endpoint: str, method: str, response_model: type[T] | None, data: dict | None = None) -> T | None:
        response = self.request(method, endpoint, json=data)
        if response.is_error:
            detail = json.loads(response.text)["detail"]
            error_type = detail["error_type"]
            error_message = detail["error_message"]
            traceback = "\n".join(detail["traceback"])
            raise httpx.HTTPStatusError(
                request=response.request, response=response, message=f"{error_type}: {error_message}\n{traceback}")

        if response_model is not None:
            return response_model(**response.json())

    def agent_get_action(self, obs: Observation) -> AgentAction:
        response = self._make_request(**SotaAgentEndpoints.GET_ACTION.request_args(obs))
        return response

    def agent_close(self) -> None:
        self._make_request(**SotaAgentEndpoints.CLOSE.request_args())

    def env_setup(self, start_url: str) -> SetupOutput:
        setup_out = self._make_request(**BrowserEndpoints.SETUP.request_args(arg=SetupInput(start_url=start_url)))
        page = connect_to_remote_session(**setup_out.exec_context_params)
        return SetupOutput(init_acts=setup_out.init_acts, exec_context=dict(
            page=page,
        ))

    def env_get_observation(self) -> SubTransition:
        response = self._make_request(**BrowserEndpoints.GET_OBSERVATION.request_args())
        return response

    def post_action(self, action: AgentAction) -> None:
        self._make_request(**BrowserEndpoints.INTERNAL_STEP.request_args(action))

    def env_close(self) -> None:
        self._make_request(**BrowserEndpoints.CLOSE.request_args())
