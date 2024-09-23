from django.shortcuts import render,redirect

# Create your views here.


# Home page view
def HomePageView(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request,"index.html")

# About view
def AboutView(request):
    return render(request,'about.html')

# Services View
def ServiceView(request):
    return render(request,'services.html')

