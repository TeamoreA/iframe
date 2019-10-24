from rest_framework.response import Response


def success_response(message, data, **kwargs):
    """
    return a formated response if request successful
    """
    return Response({
        "status": "success",
        "message": message,
        "data": data,
    }, kwargs.get('status_code'))


def error_response(message, **kwargs):
    return Response({
         "status": "error",
         "message": message,
     }, kwargs.get('status_code'))
