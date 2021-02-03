from django.contrib.auth import logout
from django.http import HttpResponse


def logout_writer(request):
    logout(request)
    return HttpResponse("You're logged out.")
