from django.urls import path
from . import views

urlpatterns = [
    path('farmer_dashboard/',views.FarmerDashboard,name='farmer_dashboard'),
    path('close_active_projects/<int:project_id>',views.CloseActiveProject,name='close_active_projects'),
    
    path('farmer_user_products/',views.FarmerProducts,name='farmer_user_products'),
    path('farmer_product_details/<int:crop_id>/',views.FarmerProductDetails,name='farmer_product_details'),
    
    path('farmer_yield_predict/',views.FarmerYieldPrediction,name='farmer_yield_predict'),
    path('predict_single_yield_results/<int:pred_id>/',views.PredictSingleYieldResult,name='predict_single_yield_results'),

    path('farmer_sustainable_management/',views.FarmerSustainabilityManagementView,name='farmer_sustain_manage'),

    path('farmer_regulatory_compliance/',views.FarmerRegulatoryComplianceView,name='farmer_regulatory_compliance'),
    
    path('farmer_user_profile/',views.FarmerProfile,name='farmer_user_profile'),   
]