from kbrainsdk.validation.common import get_payload, validate_email, validate_required_parameters
def validate_ingest_onedrive(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    required_arguments = ["email", "token", "environment", "client_id", "oauth_secret", "tenant_id"]
    validate_required_parameters(body, required_arguments)

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, environment, client_id, oauth_secret, tenant_id

def validate_ingest_sharepoint_scan(req):
    body = get_payload(req)
    host = body.get('host')
    site = body.get('site')
    token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    required_arguments = ["host", "site", "token", "environment", "client_id", "oauth_secret", "tenant_id"]
    validate_required_parameters(body, required_arguments)

    drive = body.get('drive', "")
    folder_id = body.get('folder_id', "")
    current_next_link = body.get('current_next_link', "")
    initial_run_id = body.get('initial_run_id', "")

    return host, site, token, environment, client_id, oauth_secret, tenant_id, folder_id, drive, current_next_link, initial_run_id

def validate_ingest_sharepoint_files(req):
    body = get_payload(req)
    host = body.get('host')
    site = body.get('site')
    token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    drive = body.get('drive', "")
    initial_run_id = body.get('initial_run_id', "")
    cosmos_guid = body.get('cosmos_guid', "")
    required_arguments = ["host", "site", "token", "environment", "client_id", "oauth_secret", "tenant_id", "drive", "initial_run_id", "cosmos_guid"]
    validate_required_parameters(body, required_arguments)

    folder_id = body.get('folder_id', "")
    current_next_link = body.get('current_next_link', "")
    
    return host, site, token, environment, client_id, oauth_secret, tenant_id, folder_id, drive, current_next_link, initial_run_id, cosmos_guid


def validate_ingest_status(req):
    body = get_payload(req)
    datasource = body.get('datasource')

    required_arguments = ["datasource"]
    validate_required_parameters(body, required_arguments)
    
    return datasource

def validate_ingest_pipeline_status(req):
    body = get_payload(req)
    run_id = body.get('run_id')

    required_arguments = ["run_id"]
    validate_required_parameters(body, required_arguments)

    return run_id