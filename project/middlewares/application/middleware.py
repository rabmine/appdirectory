from app.models import Application, Genre, GenreApplication
 
class ApplicationMiddleware(object):
    """
    Inserts a variable representing the current page onto the request object if
    it exists in either **GET** or **POST** portions of the request.
    """
    def process_request(self, request):
        context = {}
        context["available_apps"] = Application.objects.all().count()
        request.context = context
        
