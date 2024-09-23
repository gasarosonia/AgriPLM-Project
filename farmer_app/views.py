from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfiles
from accounts.forms import UserForm, UserProfileForm
from admin_app.models import Crop,CropFertilizerPredict,SustainabilityManagent,RegulatoryCompliance
from .models import YieldPredictions
from prediction_models.yield_model.load_yield_model import predict_yield
# Create your views here.

# Farmer dashboard View
@login_required(login_url='login')
def FarmerDashboard(request):
    page = 'farmer_dash'
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
    return render(request, 'farmer_dashboard/farmer_dashboard.html',context)


# Close or deactivate the active project
def CloseActiveProject(request,project_id):
    project = YieldPredictions.objects.get(id=project_id)
    project.is_project_active = False
    project.save()
    messages.success(request,"The project now is closed...")
    return redirect('farmer_dashboard')

# User products
@login_required(login_url='login')
def FarmerProducts(request):
    page = "user_products"
    crops = Crop.objects.all()
    context = {
        'page': page,
        'crops': crops,
    }
    return render(request,'farmer_dashboard/farmer_dashboard.html', context)


# Product details
@login_required(login_url='login')
def FarmerProductDetails(request, crop_id):
    page = "product_details"
    crop = Crop.objects.get(id=crop_id)
    context = {
        'page': page,
        'crop': crop,
    }
    return render(request,'farmer_dashboard/farmer_dashboard.html',context)

# Yield prediction part
@login_required(login_url='login')
def FarmerYieldPrediction(request):
    page = "yield_prediction"
    user_info = UserProfiles.objects.get(user_id = request.user.id)
    crop_fert_pred_info = CropFertilizerPredict.objects.filter(cell = user_info.cell).order_by('-date')[:1]
    context = {
        'page': page,
        'user_info':user_info,
        'crop_fert_pred_info':crop_fert_pred_info
    }
    return render(request,'farmer_dashboard/farmer_dashboard.html', context)

# Predict single yield result
def PredictSingleYieldResult(request, pred_id):
    # This part will bring back the prediction form view
    page = "yield_prediction"
    user_info = UserProfiles.objects.get(user_id = request.user.id)
    crop_fert_pred_info = CropFertilizerPredict.objects.filter(cell = user_info.cell).order_by('-date')[:1]

    # This will fit the data and make predictions
    page_part = "yield_predict_result"
    crop_fert_single = CropFertilizerPredict.objects.get(id=pred_id)
    # features   
    Rainfall = float(crop_fert_single.rainfall)
    Fertilizer = float(request.POST['fertilizer_amount'])
    Temperature = float(crop_fert_single.temperature)
    Nitrogen = float(crop_fert_single.nitrogen)
    Phosphorus = float(crop_fert_single.phosphorus)
    Potassium = float(crop_fert_single.potassium)
    land_size = float(request.POST['land_size'])
    amount_of_crop = float(request.POST['amount_of_crop'])
    
    # call and predict the yield results 
    yield_predictions = round(predict_yield(Rainfall,Fertilizer,Temperature,Nitrogen,Phosphorus,Potassium),2)
    # Here we have to save all data in YieldPredictions table
    yield_save_data = YieldPredictions.objects.create(
        user = user_info,
        crop_fert_pred = crop_fert_single,
        fertilizer_amount = Fertilizer,
        is_project_active = True,
        predicted_yield = yield_predictions
    )
    yield_save_data.save() 
    
    context = {
        'page': page,
        'page_part': page_part,
        'user_info':user_info,
        'crop_fert_pred_info':crop_fert_pred_info,
        'yield_predictions':yield_predictions,
        'yield_save_data':yield_save_data,
        # Pass the amount of crop and land size
        'amount_of_crop': amount_of_crop,
        'land_size': land_size,
    }
    return render(request,'farmer_dashboard/farmer_dashboard.html', context)

# faremer Sustainability Management view
@login_required(login_url='login')
def FarmerSustainabilityManagementView(request):
    page = "farmer_sustain_management"
    sustain_management = SustainabilityManagent.objects.all()
    context = {
        'page': page,
        'sustain_management':sustain_management,
    }
    return render(request,'farmer_dashboard/farmer_dashboard.html',context)\


# farmer Regulatoty compliance View
@login_required(login_url='login')
def FarmerRegulatoryComplianceView(request):
    page = "regulatory_comp"
    regulatory = RegulatoryCompliance.objects.all()
    context = {
        'page': page,
        'regulatory': regulatory
    }
    return render(request,'farmer_dashboard/farmer_dashboard.html',context)



# User profile
@login_required(login_url='login')
def FarmerProfile(request):
    page = "user_profile"
    user = User.objects.get(id = request.user.id)
    user_profile= UserProfiles.objects.get(user=user.id)
    
    user_form = UserForm(instance = user)
    user_profile_form = UserProfileForm(instance=user_profile)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST,request.FILES or None,instance = user)
        user_profile_form = UserProfileForm(request.POST,request.FILES or None,instance=user_profile)
    
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request,'Profile updated successfully')
            return redirect('farmer_user_profile')
        else:
            messages.error(request,'Something went wrong! Please try again.')
            return redirect('farmer_user_profile')
    context = {
        'page': page,
        'user_profile':user_profile,
        'user_form':user_form,
        'user_profile_form':user_profile_form
    }
    return render(request,'farmer_dashboard/farmer_dashboard.html', context)