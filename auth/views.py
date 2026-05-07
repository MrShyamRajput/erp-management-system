from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)

        user = authenticate(request, username=username, password=password)
        print("user",user)
        print("AUTH RESULT:", user)
        User = get_user_model()

        print("USER EXISTS:", User.objects.filter(username=username).exists())
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
            print("reditecting")
        else:
            messages.error(request, "Invalid Email or password")
    
    return render(request, "auth/login.html")


User = get_user_model()


@login_required
def create_user(request):
    users = User.objects.all()
    show_modal = False  # 🔥 default

    # 🔐 Permission check
    if request.user.role not in ["admin", "hr"] and not request.user.is_superuser:
        messages.error(request, "❌ No permission to create user")
        return render("usermanagement.html")

    if request.method == "POST":
        show_modal = True  # 🔥 keep modal open on error

        username = request.POST.get("username")

        # ✅ Duplicate check
        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ Username already exists")
        else:
            user = User.objects.create_user(
                username=username,
                email=request.POST.get("email"),
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                password=request.POST.get("password"),
                role=request.POST.get("role"),
                phone=request.POST.get("phone"),
            )
            print("name",username)
            user.is_active = request.POST.get("is_active") == "on"

            if request.FILES.get("profile_image"):
                user.profile_image = request.FILES["profile_image"]

            user.save()

            messages.success(request, "✅ User created successfully")
        
            return redirect("userManagement",)  # 🔥 success → reload & close modal

    context = {
        "users": users,
        "show_modal": show_modal
    }

    return render(request, "usermanagement.html", context)