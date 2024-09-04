
from kbrainsdk.validation.common import get_payload, validate_email, validate_required_parameters


def validate_user_entra_groups(req):
    body = get_payload(req)
    required_arguments = ["email", "token", "client_id", "oauth_secret", "tenant_id"]
    validate_required_parameters(body, required_arguments)
    
    email = body.get('email')
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, client_id, oauth_secret, tenant_id

def validate_list_group_members(req):
    body = get_payload(req)
    required_arguments = ["group_id", "email", "token", "client_id", "oauth_secret", "tenant_id"]
    validate_required_parameters(body, required_arguments)

    group_id = body.get('group_id')
    email = body.get('email')
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    continuation_token = body.get('continuation_token', None)

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return group_id, email, token, client_id, oauth_secret, tenant_id, continuation_token