from kbrainsdk.validation.common import get_payload, validate_required_parameters

def validate_servicebus_message(req):
    body = get_payload(req)
    required_arguments = ["message", "topic_name", "application_properties"]
    validate_required_parameters(body, required_arguments)

    message = body.get('message')
    topic_name = body.get('topic_name')
    application_properties = body.get('application_properties')    

    return message, topic_name, application_properties