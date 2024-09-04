from typing import Any
from kbrainsdk.validation.events import validate_servicebus_message
from kbrainsdk.apibase import APIBase

class Events(APIBase):

    def __init__(self, *args: Any, **kwds: Any) -> Any:
        return super().__init__(*args, **kwds)
    
    def publish_message(self, message: str, topic_name: str, application_properties: dict | None = None) -> None:
        payload = {
            "message": message,
            "topic_name": topic_name,
            "application_properties": application_properties
        }
        
        validate_servicebus_message(payload)
        path = f"/service_bus/send/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response