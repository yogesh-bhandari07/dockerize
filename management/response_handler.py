from rest_framework.response import Response


from rest_framework.views import exception_handler


def custom_response(
    success=True, message="Operation successful", data=None, status=200
):
    response = {"success": success, "message": message, "data": data}
    return Response(response, status=status)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        custom_data = {
            "success": False,
            "message": response.data.get("detail", "An error occurred"),
            "data": None,
        }
        response.data = custom_data
    return response
