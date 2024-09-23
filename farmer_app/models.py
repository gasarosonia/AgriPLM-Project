from django.db import models
from accounts.models import UserProfiles
from admin_app.models import CropFertilizerPredict

# Create your models here.
class YieldPredictions(models.Model):
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE)
    crop_fert_pred = models.ForeignKey(CropFertilizerPredict, on_delete=models.CASCADE)
    yield_pred_date = models.DateField(auto_now_add=True)
    fertilizer_amount = models.FloatField()
    is_project_active = models.BooleanField(default=False)
    predicted_yield = models.FloatField(default=0.0,null=True,blank=True)
    
    def __str__(self):
        return f"{self.user.user.username} - {self.yield_pred_date}"
    
    class Meta:
        verbose_name_plural = 'YieldPredictions'
    