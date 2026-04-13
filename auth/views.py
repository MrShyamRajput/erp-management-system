from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from signal import getsignal

# Create your views here.
def login_page(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        user=authenticate(request,username=email,password=password)

        if user is not None:
            login(request, user)  

            role=getattr(user,"role",None)

            if user.is_superuser:
                return redirect()
    return render(request,"auth/login.html")