from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfiles
from accounts.forms import UserForm, UserProfileForm
from .forms import CropForm,CropPredictForm,RegulatoryComplianceForm, SustainabilityManagentForm
from .models import Crop,CropFertilizerPredict,RegulatoryCompliance, SustainabilityManagent,Notification
from farmer_app.models import YieldPredictions
# Import aggregation models function
from django.db.models import Sum,Func,FloatField

# Import prediction model
from prediction_models.crop_model.load_crop_model import predict_crop
from prediction_models.fertilizer_model.load_fertilizer_model import predict_fertilizer

# Create your views here.

# Admin dashboard view
@login_required(login_url='login')
def AdminDashboardView(request):
    page = 'admin_dash'
    farmers = UserProfiles.objects.filter(title='farmer')
    number_of_farmers = farmers.count()
    
    yield_data = YieldPredictions.objects.all()
   
    # Let's calculate total_yields, number of active and closed projects
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
        'number_of_farmers':number_of_farmers,
        'total_yields':round(total_yields,2),
        'active_projects':active_projects,
        'closed_projetcs':closed_projetcs,
        'aggre_query':aggre_query,
    }
    return render(request,'admin_dashboard/admin_dashboard.html', context)


# Admin Products view
def AdminProductView(request):
    page = "admin_products"
    crops = Crop.objects.all()
    if request.method == 'POST':
        crop_image = request.FILES.get('crop_image')
        crop_name = request.POST.get('crop_name')
        description = request.POST.get('description')
        planting_time = request.POST.get('planting_time')
        fertilizer = request.POST.get('fertilizer')
        irrigation = request.POST.get('irrigation')
        harvest = request.POST.get('harvest')
        cleaning = request.POST.get('cleaning')
        storage = request.POST.get('storage')
        transportation = request.POST.get('transportation')
        consumption = request.POST.get('consumption')
        end_of_life = request.POST.get('end_of_life')
        
        crops  = Crop.objects.create(
            crop_image = crop_image,
            crop_name = crop_name,
            description = description,
            planting_time = planting_time,
            fertilizer = fertilizer,
            irrigation = irrigation,
            harvest = harvest,
            cleaning = cleaning,
            storage = storage,
            transportation =transportation,
            consumption = consumption,
            end_of_life = end_of_life                
            ) 
        if True:              
            crops.save()
            notification = Notification.objects.create(
                    name = "New Crop Arrival..."
                )
            notification.save()
            messages.success(request,'Crops saved successfully!')
            return redirect('admin_products')
        
    context = {
        'page': page,
        'crops': crops,
    }
    return render(request,'admin_dashboard/admin_dashboard.html',context)


# Product or Crop details
def CropDetailsView(request, crop_id):
    page = "product_details"
    crop = get_object_or_404(Crop, id=crop_id)
    crop_form = CropForm(instance=crop)
    if request.method == 'POST':
        crop_form = CropForm(request.POST,request.FILES, instance=crop)
        if crop_form.is_valid():
            crop_form.save()
            messages.success(request,'Crop details updated successfully!')
            return redirect('crop_details', crop_id=crop_id)
    context = {
        'page': page,
        'crop': crop,
        'crop_form': crop_form
    }
    return render(request,'admin_dashboard/admin_dashboard.html',context)


# Delete a crop
def DeleteCropView(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    crop.delete()
    messages.success(request,'Crop deleted successfully!')
    return redirect('admin_products')
   


# Crop and Fertilizer prediction page View and predict Crop form
def CropPredictionView(request):
    page = 'crop_fertilizer_predict'
    part = 'crop_prediction_part'
    cropFertilizerModel = CropFertilizerPredict.objects.all().order_by('-id')
    cropPredictForm = CropPredictForm()

    context = {
        'page': page,
        'part': part,
        'cropFertilizerModel': cropFertilizerModel,
        'cropPredictForm': cropPredictForm
    }
    return render(request,'admin_dashboard/admin_dashboard.html',context)

# Predict single crop prediction
def PredictSingleCropResultView(request):
    # If request is POST, it will make Crop prediction 
    page = 'crop_fertilizer_predict'
    part_page = 'crop_result_page'
    cropPredictForm = CropPredictForm(request.POST)
    if cropPredictForm.is_valid():
        cell = cropPredictForm.cleaned_data['cell']
        nitrogen = int(cropPredictForm.cleaned_data['nitrogen'])
        phosphorus = int(cropPredictForm.cleaned_data['phosphorus'])
        potassium = int(cropPredictForm.cleaned_data['potassium'])
        ph = float(cropPredictForm.cleaned_data['ph'])
        rainfall = int(cropPredictForm.cleaned_data['rainfall'])
        temperature = int(cropPredictForm.cleaned_data['temperature'])
        
        # call predict defined method
        crop_result = predict_crop(nitrogen,phosphorus,potassium,ph,rainfall,temperature)
        
        cropFertilizerPredict = CropFertilizerPredict.objects.create(
            cell = cell,
            nitrogen = nitrogen,
            phosphorus = phosphorus,
            potassium = potassium,
            ph = ph,
            rainfall =rainfall,
            temperature = temperature,
            predicted_crop = crop_result
        )
        cropFertilizerPredict.save()
        crop_result = CropFertilizerPredict.objects.get(id=cropFertilizerPredict.id)
        
        context = {
            'page': page,
            'part_page': part_page,
            'crop_result': crop_result,
        }
        return render(request,'admin_dashboard/admin_dashboard.html',context)

# Fertilizer prediction view
def FertilizerPredictionView(request):
    page = 'crop_fertilizer_predict'
    part = 'fertilizer_prediction_part'
    cropFertilizerModel = CropFertilizerPredict.objects.all().order_by('-id')
    
    context = {
        'page': page,
        'part': part,
        'cropFertilizerModel': cropFertilizerModel,
    }
    return render(request,'admin_dashboard/admin_dashboard.html',context)


# Fertilizer prediction View
def PredictSingleFertilizerView(request,crop_pred_id):
    page = 'crop_fertilizer_predict'
    part_page = 'predict_fertilizer'
    crop = get_object_or_404(CropFertilizerPredict,pk=crop_pred_id)
    # load columns to be fitted in fertilizer model
    Nitrogen = crop.nitrogen
    Phosphorus = crop.phosphorus
    Potassium = crop.potassium
    ph = crop.ph
    Rainfall = crop.rainfall
    Temperature = crop.temperature
    predicted_crop = crop.predicted_crop
    
    # call Fertilizer prediction model
    fertilizer_result = predict_fertilizer(Nitrogen,Phosphorus,Potassium,
                                           ph,Rainfall,Temperature,predicted_crop)
    
    crop.predicted_fertilizer = fertilizer_result
    crop.save()
    
    context = {
        'page': page,
        'crop': crop,
        'part_page': part_page,
    }
    messages.success(request,f"The recommended fertilizer is.. {fertilizer_result}...")
    return render(request,'admin_dashboard/admin_dashboard.html',context)  
    

# Sustainability Management view
@login_required(login_url='login')
def SustainabilityManagementView(request):
    page = "sustain_management"
    sustain_management = SustainabilityManagent.objects.all()
    sustain_management_form = SustainabilityManagentForm()
    if request.method == 'POST':
        sustain_management_form = SustainabilityManagentForm(request.POST)
        if sustain_management_form.is_valid():
            title = sustain_management_form.cleaned_data['title']
            description = sustain_management_form.cleaned_data['description']
            sustain_management = SustainabilityManagent.objects.create(
                title=title,
                description=description,
            )
            sustain_management.save() 
            notification = Notification.objects.create(
                    name = "New Sustain Management..."
                )
            notification.save()           
            messages.success(request,f'{title} Added Successfully!')
            return redirect('sustain_management')
        else:
            messages.error(request,'Something went wrong! Please try again!')
            return redirect('sustain_management')
    context = {
        'page': page,
        'sustain_management':sustain_management,
        'sustain_management_form':sustain_management_form
    }
    return render(request,'admin_dashboard/admin_dashboard.html',context)


# update sustainability management
@login_required(login_url='login')
def UpdateStainabilityMamnagementView(request,sustain_id):
    page = 'sustain_manage_update'
    sustain_manage = get_object_or_404(SustainabilityManagent,pk=sustain_id)
    sustain_management_form = SustainabilityManagentForm(instance=sustain_manage)

    if request.method == 'POST':
        sustain_management_form = SustainabilityManagentForm(request.POST,instance=sustain_manage)
        if sustain_management_form.is_valid():
            sustain_management_form.save(commit=True)
            messages.success(request,f'{sustain_manage.title} Updated Successfully!')
            return redirect('sustain_management')
        else:
            messages.error(request,'Something went wrong! Please try again!')
            return redirect('sustain_management')

    context = {
        'sustain_management_form':sustain_management_form,
        'sustain_manage':sustain_manage,
        'page':page
    }
    return render(request,'admin_dashboard/admin_dashboard.html',context)

# Delete DeleteRegulatoryComplianceView
@login_required(login_url='login')
def DeleteStainabilityMamnagementView(request,sustain_id):
    sustain = get_object_or_404(SustainabilityManagent, pk=sustain_id)
    sustain.delete()
    messages.success(request,'Deleted Successfully!')
    return redirect('sustain_management')

# Regulatoty compliance View
@login_required(login_url='login')
def RegulatoryComplianceView(request):
    page = "regulatory_comp"
    regulatory_comp_form = RegulatoryComplianceForm()
    regulatory = RegulatoryCompliance.objects.all()
    if request.method == 'POST':
        regulatory_comp_form = RegulatoryComplianceForm(request.POST)
        if regulatory_comp_form.is_valid():
            title = regulatory_comp_form.cleaned_data['title']
            description = regulatory_comp_form.cleaned_data['description']
            
            regulatory = RegulatoryCompliance.objects.create(
                title=title,
                description=description,
            )
            regulatory.save()
            notification = Notification.objects.create(
                    name = "New Policy added..."
                )
            notification.save()            
            messages.success(request,'Regulatory Compliance Added Successfully!')
            return redirect('regulatory_comp')
        else:
            messages.error(request,'Something went wrong! Please try again!')
            return redirect('regulatory_comp')
    context = {
        'page': page,
        'regulatory_comp_form':regulatory_comp_form,
        'regulatory': regulatory
    }
    return render(request,'admin_dashboard/admin_dashboard.html',context)


# Update Regulatory Compliance
@login_required(login_url='login')
def UpdateRegulatoryComplianceView(request,pk):
    page = "regulatory_comp_update"
    regulatory = get_object_or_404(RegulatoryCompliance, pk=pk)
    
    regulatory_comp_update_form = RegulatoryComplianceForm(instance=regulatory)
    if request.method == 'POST':
        regulatory_comp_update_form = RegulatoryComplianceForm(request.POST, instance=regulatory)
        if regulatory_comp_update_form.is_valid():
            regulatory_comp_update_form.save(commit=True)
            notification = Notification.objects.create(
                    name = "Policy updated..."
                )
            notification.save()
            messages.success(request,f'{regulatory.title} Updated Successfully!')
            return redirect('regulatory_comp')
        else:
            messages.error(request,'Something went wrong! Please try again!')
            return redirect('regulatory_comp')
    context = {
        'page': page,
       'regulatory_comp_update_form': regulatory_comp_update_form,
       'regulatory': regulatory
    }
    return render(request,'admin_dashboard/admin_dashboard.html', context)


# Delete DeleteRegulatoryComplianceView
@login_required(login_url='login')
def DeleteRegulatoryComplianceView(request,pk):
    regulatory = get_object_or_404(RegulatoryCompliance, pk=pk)
    regulatory.delete()
    messages.success(request,'Deleted Successfully!')
    return redirect('regulatory_comp')


# Estimated Farmers Yield Report View
@login_required(login_url='login')
def EstimatedYieldReportView(request):
    page = 'yield_report'
    yield_data = YieldPredictions.objects.all()
    number_of_projects = yield_data.count()
    context ={
        'page':page,
        'yield_data':yield_data,
        'number_of_projects':number_of_projects,
    }
    return render(request,'admin_dashboard/admin_dashboard.html',context)

# admin User profile view
@login_required(login_url='login')
def AdminProfileView(request):
    page = "user_profile"
    user = User.objects.get(id = request.user.id)
    notifications = Notification.objects.all().order_by('-id')
    notification_count = notifications.count()
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
            return redirect('admin_profile')
        else:
            messages.error(request,'Something went wrong! Please try again.')
            return redirect('admin_profile')
    context = {
        'page': page,
        'user_profile':user_profile,
        'user_form':user_form,
        'user_profile_form':user_profile_form,
        'notifications': notifications,
        'notification_count': notification_count
    }
    return render(request,'admin_dashboard/admin_dashboard.html', context)

# Delete notification
def DeleteNotificationView(request,notif_id):
    notification = get_object_or_404(Notification, pk=notif_id)
    notification.delete()
    return redirect('admin_profile')