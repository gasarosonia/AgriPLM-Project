from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/',views.AdminDashboardView, name='admin_dash'),
    path('admin_products/',views.AdminProductView, name='admin_products'),
    path('admin_crop_details/<int:crop_id>/',views.CropDetailsView, name='crop_details'),
    path('admin__delete_crop_details/<int:crop_id>/',views.DeleteCropView, name='delete_crop'),
    
    path('crop_prediction/',views.CropPredictionView,name='crop_pred'),
    path('predict_crop_results/',views.PredictSingleCropResultView, name='predict_crop_results'),
    path('fertilizer_prediction/',views.FertilizerPredictionView,name='fert_pred'),
    path('predict_fertilizer/<int:crop_pred_id>/',views.PredictSingleFertilizerView,name='predict_fertilizer'),
    
    path('sustainable_management/',views.SustainabilityManagementView,name='sustain_management'), 
    path('update_sustainable_management/<int:sustain_id>/',views.UpdateStainabilityMamnagementView,name='update_sustain'),
    path('delete_sustainable_management/<int:sustain_id>/',views.DeleteStainabilityMamnagementView, name='delete_sustain'),
       
    path('regulatory_compliance/',views.RegulatoryComplianceView, name='regulatory_comp'),
    path('update_regulatory/<int:pk>/',views.UpdateRegulatoryComplianceView, name='regulatory_update'),
    path('delete_regulatory/<int:pk>/',views.DeleteRegulatoryComplianceView, name='delete_reg'),
    
    path('estimated_yield_reporter/',views.EstimatedYieldReportView, name='estimated_yield_reporter'),
    
    path('admin_profile/',views.AdminProfileView, name='admin_profile'),
    path('delete_notification/<int:notif_id>/',views.DeleteNotificationView, name='delete_notification'),
]