from typing import Literal

import pydantic


class Endpoint(pydantic.BaseModel):
    prefix: str
    path: str
    method: Literal["GET", "POST"]
    response_model: type[pydantic.BaseModel] | None
    request_model: type[pydantic.BaseModel] | None

    def request_args(self, arg: pydantic.BaseModel | None = None):
        if arg is None:
            return dict(endpoint=self.prefix + self.path, method=self.method, response_model=self.response_model)

        assert isinstance(arg, self.request_model)
        dt = arg.model_dump()
        return dict(endpoint=self.prefix + self.path, method=self.method, response_model=self.response_model, data=dt)
