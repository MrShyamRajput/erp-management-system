from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request,'dashboard.html')

def userManagement(request):
    return render(request,'userManagement.html')

def hrManagement(request):
    return render(request,'hrmanagement.html')