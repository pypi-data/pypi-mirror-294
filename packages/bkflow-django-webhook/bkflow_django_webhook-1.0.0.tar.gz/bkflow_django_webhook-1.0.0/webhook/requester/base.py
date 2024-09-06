# -*- coding: utf-8 -*-
import logging

import requests
from pydantic import BaseModel

logger = logging.getLogger(__name__)

JSON_CONTENT_TYPE = "application/json"
FORM_CONTENT_TYPE = "application/x-www-form-urlencoded"


class RequestConfig(BaseModel):
    url: str
    method: str = "post"
    content_type: str = JSON_CONTENT_TYPE
    headers: dict = None
    data: dict = {}  # convert to json when content_type is JSON_CONTENT_TYPE
    verify: bool = False
    timeout: int = None

    @staticmethod
    def _gen_default_headers(content_type):
        return {"Content-Type": content_type}

    def __init__(self, **kwargs):
        kwargs["headers"] = {
            **self._gen_default_headers(content_type=kwargs.get("content_type", JSON_CONTENT_TYPE)),
            **kwargs.get("headers", {}),
        }
        super().__init__(**kwargs)

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        content_type = result.pop("content_type")
        if content_type == JSON_CONTENT_TYPE:
            result["json"] = result.pop("data")
        return result


class RequestResult(BaseModel):
    result: bool
    response: requests.Response = None
    exe_data: str = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def ok(self):
        return self.result and self.response.ok

    @property
    def response_status_code(self):
        if self.response is None:
            return None
        return self.response.status_code

    def json_response(self):
        if self.response is None:
            return None
        try:
            return self.response.json()
        except Exception as e:
            logger.exception(f"[RequestResult.json_response error] {e}")
            return self.response.text


class Requester:
    def __init__(self, config: RequestConfig):
        self.request_config = config

    def request(self, *args, **kwargs) -> RequestResult:
        try:
            response = requests.request(**self.request_config.dict())
        except Exception as e:
            logger.exception(f"[Requester.request error] {e}")
            return RequestResult(result=False, exe_data=str(e))
        else:
            return RequestResult(result=True, response=response)
