from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


@login_required(login_url="login")
def index(request):
    user = request.user
    return render(request, "dashboard/index.html", {"user": user})
