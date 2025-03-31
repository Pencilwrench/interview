from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def home(request):
    # redirect to django admin
    response = HttpResponseRedirect(reverse("admin:index"))
    return response
    