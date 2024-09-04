import pydantic

from silverriver.client.endpoint import Endpoint
from silverriver.interfaces import AgentAction, Observation


class SotaAgentConfig(pydantic.BaseModel):
    max_retry: int = 4
    llm_name: str = "gpt-4o"


class SotaAgentEndpoints:
    PREFIX = "/api/v1/sota_agent"

    GET_ACTION = Endpoint(prefix=PREFIX, path="/get_action", method="POST", response_model=AgentAction, request_model=Observation)
    CLOSE = Endpoint(prefix=PREFIX, path="/close", method="POST", response_model=None, request_model=None)
