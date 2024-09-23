from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfiles
from .forms import UserTitleForm
from farmer_app.models import YieldPredictions

# Import aggregation models function
from django.db.models import Sum,Func,FloatField

# Call Notification model
from admin_app.models import Notification
# Create your views here

# Registration form view
def FarmerRegisterView(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username= username).exists():
                messages.error(request,'Username already exist!')
                return redirect('register')
            
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email already exist!')
                return redirect('register')
            
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
                user.save()
                notification = Notification.objects.create(
                    name = "New Farmer Registered..."
                )
                notification.save()
                messages.success(request,'Registration successful!')
                return redirect('login')

        else:
            messages.error(request,'Passwords do not match!')
            return redirect('register')
                
    context = {}
    return render(request,'accounts/farmer_signup.html',context)

# Login form view
def LoginView(request):
    user_title_form = UserTitleForm()
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_title_form = UserTitleForm(request.POST)

        user = authenticate(username=username, password=password)
        
        if user is not None and user_title_form.is_valid():
            user_title = user_title_form.cleaned_data['title']
            if UserProfiles.objects.filter(user=user.id,title=user_title):
                login(request, user)
                messages.success(request,"Login successful!")
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid Credentials')
            return redirect('login')
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect('login')
            
    context = {'user_title_form':user_title_form}
    return render(request,'accounts/user_login.html',context)


# Logout view
def LogoutView(request):
    logout(request)
    messages.success(request,'Logout successful!')
    return redirect('login')

# Dashboard logic handling view
@login_required(login_url='login')
def DashboardView(request):
    if not request.user.is_superuser:
        if UserProfiles.objects.filter(user=request.user.id, title = 'farmer'):
            page = 'farmer_dash'
            # This will show the farmer yield reports
            user = UserProfiles.objects.get(user=request.user.id)
            yield_data = YieldPredictions.objects.filter(user = user)
            
            my_total_yields = 0
            my_active_projects = 0
            my_closed_projetcs = 0
            for data in yield_data:
                if data.is_project_active:
                    my_total_yields += data.predicted_yield  
                    my_active_projects += 1
                else:
                    my_closed_projetcs += 1
                    
            context = {
                'page': page,
                'yield_data':yield_data,
                'my_total_yields':round(my_total_yields,2),
                'my_active_projects':my_active_projects,
                'my_closed_projetcs':my_closed_projetcs,
            }
            return render(request,'farmer_dashboard/farmer_dashboard.html',context)
        
        elif UserProfiles.objects.filter(user=request.user.id, title = 'admin'):
            page = 'admin_dash'
            farmers = UserProfiles.objects.filter(title='farmer')
            number_of_farmers = farmers.count()
            yield_data = YieldPredictions.objects.all()
    
            total_yields = 0
            active_projects = 0
            closed_projetcs = 0
            for data in yield_data:
                if data.is_project_active:
                    total_yields += data.predicted_yield 
                    active_projects += 1
                else:
                    closed_projetcs += 1
            
            # Let's perform the aggregation method like sum, percentage
            # We have to find the sum of predicted_yields of all active projects
            percentage_query = YieldPredictions.objects.filter(is_project_active=True)
            sum_of_active_predicted_yield = 0
            for query in percentage_query:
                sum_of_active_predicted_yield+= query.predicted_yield
            
            # Inside here we have to calculate the sum or total predicted yield for each grouped crop
            class Round(Func):
                function = 'ROUND'
                arity = 2
                output_field = FloatField()
                
            aggre_query = YieldPredictions.objects.values('crop_fert_pred__predicted_crop').filter(is_project_active=True).annotate(
                sum =Sum('predicted_yield'),percentage=Round((Sum('predicted_yield')/sum_of_active_predicted_yield)*100,2))
            
                  
            context = {
                'page': page,
                'number_of_farmers': number_of_farmers,
                'total_yields':round(total_yields,2),
                'active_projects':active_projects,
                'closed_projetcs':closed_projetcs,
                'aggre_query':aggre_query,
            }
            return render(request,'admin_dashboard/admin_dashboard.html',context)
                
        else:   
         return redirect('home')
    else:
        return HttpResponseRedirect('/admin')
        # redirect('home')