from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import students
# Create your views here.


def landing(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'login.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('index')
        messages.error(request, "Invalid username or password.")
    return redirect('landing')


def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('landing')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('landing')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('landing')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Registration successful. You are now logged in.")
        return redirect('index')
    return redirect('landing')


def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('landing')


@login_required(login_url='landing')
def index(request):
    data = students.objects.all()
    context = {
        'data': data,
        'total_students': data.count(),
        'avg_age': round(sum(item.age for item in data) / data.count(), 1) if data else 0,
        'male_count': data.filter(gender__iexact='male').count(),
        'female_count': data.filter(gender__iexact='female').count(),
    }
    return render(request, 'index.html', context)


@login_required(login_url='landing')
def insertdata(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        student = students(name=name, age=age, email=email, gender=gender)
        student.save()
        return redirect('index')
    return redirect('index')


@login_required(login_url='landing')
def updatedata(request,id):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        edit=students.objects.get(id=id)
        edit.name = name
        edit.age = age
        edit.email = email
        edit.gender = gender
        edit.save()
        return redirect('index')
    d = students.objects.get(id=id)
    context = {
        'd': d
    }
    return render(request, 'edit.html', context)


@login_required(login_url='landing')
def deletedata(request, id):
    d = students.objects.get(id=id)
    d.delete()
    return redirect('index')


@login_required(login_url='landing')
def store(request):
    products = [
        {"name": "Urban Runner Shoes", "category": "Footwear", "price": 89, "old_price": 119, "rating": 4.7, "badge": "Best Seller"},
        {"name": "Nova Smartwatch X2", "category": "Wearables", "price": 149, "old_price": 199, "rating": 4.8, "badge": "New"},
        {"name": "Aero Noise-Cancel Buds", "category": "Audio", "price": 69, "old_price": 99, "rating": 4.6, "badge": "Hot Deal"},
        {"name": "Flex Gym Duffel", "category": "Bags", "price": 55, "old_price": 75, "rating": 4.5, "badge": "Limited"},
        {"name": "Luxe Cotton Hoodie", "category": "Apparel", "price": 45, "old_price": 60, "rating": 4.4, "badge": "Top Rated"},
        {"name": "Hydro Steel Bottle", "category": "Lifestyle", "price": 29, "old_price": 39, "rating": 4.9, "badge": "Editor Pick"},
    ]
    return render(request, 'myapp/store.html', {'products': products})
