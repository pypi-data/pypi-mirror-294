from typing import Any, Dict
from kbrainsdk.apibase import APIBase
from kbrainsdk.validation.signalr import (
    validate_signalr_broadcast, 
    validate_signalr_group_broadcast,
    validate_signalr_subscription_request,
    validate_signalr_group_create_request
)

class SignalR(APIBase):

    def __init__(self, *args: Any, **kwds: Any) -> Any:
        return super().__init__(*args, **kwds)
    
    def broadcast(self, 
        target:str, 
        action: Dict[str, Any], 
        token:str
    ):
        payload = {
            "target": target,
            "action": action,
            "token": token
        }
        validate_signalr_broadcast(payload)
        path = f"/websocket/broadcast/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def group_broadcast(self, 
        group_name:str, 
        action: Dict[str, Any], 
        client_id: str,
        tenant_id: str,
        client_secret: str
    ):
        payload = {
            "group_name": group_name,
            "action": action,
            "client_id": client_id,
            "tenant_id": tenant_id,
            "client_secret": client_secret
        }
        validate_signalr_group_broadcast(payload)
        path = f"/websocket/group/broadcast/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def subscribe_to_websocket_group(self, token: str, subscription_id:str, group_name: str, client_id: str, tenant_id: str, client_secret: str):
        payload = {
            "subscription_id": subscription_id,
            "token": token,
            "group_name": group_name,
            "client_id": client_id,
            "tenant_id": tenant_id,
            "client_secret": client_secret
        }
        validate_signalr_subscription_request(payload)
        path = f"/websocket/group/subscribe/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def unsubscribe_to_websocket_group(self, token: str, group_name: str, subscription_id: str, client_id: str, tenant_id: str, client_secret: str):
        payload = {
            "token": token,
            "group_name": group_name,
            "subscription_id": subscription_id,
            "client_id": client_id,
            "tenant_id": tenant_id,
            "client_secret": client_secret
        }
        validate_signalr_subscription_request(payload)
        path = f"/websocket/group/unsubscribe/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def create_group(self, group_name:str, group_data:dict, client_id: str, tenant_id: str, client_secret: str):
        payload = {        
            "group_name": group_name,
            "group_data": group_data,
            "client_id": client_id,
            "tenant_id": tenant_id,
            "client_secret": client_secret
        }
        validate_signalr_group_create_request(payload)
        path = f"/websocket/group/create/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response