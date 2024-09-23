from django.contrib import admin
from .models import RegulatoryCompliance, SustainabilityManagent,Crop,CropFertilizerPredict,Notification
# Register your models here.

admin.site.register(RegulatoryCompliance)
admin.site.register(SustainabilityManagent)
admin.site.register(Crop)

admin.site.register(CropFertilizerPredict)
admin.site.register(Notification)