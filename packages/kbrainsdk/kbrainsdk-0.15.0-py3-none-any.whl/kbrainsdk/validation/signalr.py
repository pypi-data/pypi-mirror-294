from kbrainsdk.validation.common import get_payload, validate_required_parameters

def validate_signalr_broadcast(req):
    body = get_payload(req)
    required_arguments = ["target", "action", "token"]
    validate_required_parameters(body, required_arguments)

    target = body.get('target')
    action = body.get('action')
    token = body.get('token')
    
    return target, action, token

def validate_signalr_group_broadcast(req):
    body = get_payload(req)
    required_arguments = ["group_name", "action", "client_id", "tenant_id", "client_secret"]
    validate_required_parameters(body, required_arguments)

    group_name = body.get('group_name')
    action = body.get('action')
    client_id = body.get('client_id')
    tenant_id = body.get('tenant_id')
    client_secret = body.get('client_secret')
    
    return group_name, action, client_id, tenant_id, client_secret

def validate_signalr_group_request(req):
    body = get_payload(req)
    required_arguments = ["token", "group_name", "client_id", "tenant_id", "client_secret"]
    validate_required_parameters(body, required_arguments)

    token = body.get('token')
    client_id = body.get('client_id')
    tenant_id = body.get('tenant_id')
    group_name = body.get('group_name')
    client_secret = body.get('client_secret')

    return token, group_name, client_id, tenant_id, client_secret

def validate_signalr_subscription_request(req):
    body = get_payload(req)
    required_arguments = ["token", "group_name", "subscription_id", "client_id", "tenant_id", "client_secret"]
    validate_required_parameters(body, required_arguments)

    token = body.get('token')
    client_id = body.get('client_id')
    tenant_id = body.get('tenant_id')
    group_name = body.get('group_name')
    subscription_id = body.get('subscription_id')
    client_secret = body.get('client_secret')

    return token, group_name, subscription_id, client_id, tenant_id, client_secret


def validate_signalr_group_create_request(req):
    body = get_payload(req)
    required_arguments = ["group_name", "group_data", "client_id", "tenant_id", "client_secret"]
    validate_required_parameters(body, required_arguments)

    group_name = body.get('group_name')
    group_data = body.get('group_data')
    client_id = body.get('client_id')
    tenant_id = body.get('tenant_id')
    client_secret = body.get('client_secret')
                            
    return group_name, group_data, client_id, tenant_id, client_secret