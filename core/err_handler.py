from django.contrib import messages
from django.shortcuts import render
from django.views import View

class CommonErrorHandlerView(View):
    """
    Handle common errors
    """

    template_name = 'err_handler.html'

    def get(self, request, exception=None):
        """
        Handle common errors logic
        """
        status_code = 500
        if hasattr(exception, 'status_code'):
            status_code = getattr(exception, 'status_code', 500)

        if hasattr(exception, 'message'):
            messages.error(request, str(exception))
        else:
            messages.error(request, f'An error occured {status_code}')

        context = {
            'status_code': status_code,
            'message': {
                400: 'Bad Request',
                401: 'Unauthorized',
                403: 'Forbidden',
                404: 'Not Found',
                503: 'Service Unavailable',
                500: 'Internal Server Error',
            }.get(status_code, 'Unknown Error'),
        }

        return render(request, self.template_name, context, status=status_code)
