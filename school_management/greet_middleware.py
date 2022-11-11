import result.views

class Greet:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Welcome to the School Management System")
        response = self.get_response(request)
        print("Thanks for using this app.")

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.view_class is result.views.Result:
            print("You have entered the result section")
        return None
