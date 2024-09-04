from kbrainsdk.validation.users import validate_user_entra_groups, validate_list_group_members
from kbrainsdk.apibase import APIBase

class User(APIBase):
    
    def user_entra_groups(self, email, token, client_id, oauth_secret, tenant_id):    
            payload = {
                "email": email,
                "token": token,
                "client_id": client_id,
                "oauth_secret": oauth_secret,
                "tenant_id": tenant_id
            }
    
            validate_user_entra_groups(payload)
    
            path = f"/user/entra/groups/v1"
            response = self.apiobject.call_endpoint(path, payload, "post")
            return response

    
    def list_group_members(self, group_id, email, token, client_id, oauth_secret, tenant_id, continuation_token=None):    
            payload = {
                "group_id": group_id,
                "email": email,
                "token": token,
                "client_id": client_id,
                "oauth_secret": oauth_secret,
                "tenant_id": tenant_id,
            }
    
            validate_list_group_members(payload)
    
            if continuation_token:
                payload["continuation_token"] = continuation_token
                
            path = f"/user/list/groups/list/v1"
            response = self.apiobject.call_endpoint(path, payload, "post")
            return response

            