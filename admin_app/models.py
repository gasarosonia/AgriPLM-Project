from django.db import models

# Create your models here.
MUSHA_CELL_CHOICES =(
    ('Kagarama','Kagarama'),
    ('Nyakabanda','Nyakabanda'),
    ('Musha','Musha'),
    ('Akabare','Akabare'),
    ('Nyabisindu','Nyabisindu'),
    ('Budahanda','Budahanda')
)
    
# Model of crops
class Crop(models.Model):
    crop_image = models.ImageField(upload_to='crop_pictures')
    crop_name = models.CharField(max_length=100)
    description = models.TextField()
    planting_time = models.TextField()
    fertilizer = models.TextField()
    irrigation = models.TextField()
    harvest = models.TextField()
    cleaning = models.TextField()
    storage = models.TextField()
    transportation = models.TextField()
    consumption = models.TextField()
    end_of_life = models.TextField()
    
    def __str__(self):
        return self.crop_name
    
# Crop and Fertilizer prediction Model
class CropFertilizerPredict(models.Model):
    cell = models.CharField(max_length=100,choices=MUSHA_CELL_CHOICES)
    date = models.DateField(auto_now_add=True)
    nitrogen = models.IntegerField()
    phosphorus = models.IntegerField()
    potassium = models.IntegerField()
    ph = models.FloatField()
    rainfall = models.IntegerField()
    temperature = models.IntegerField()
    predicted_crop = models.CharField(max_length=100)
    predicted_fertilizer = models.CharField(max_length=100, blank=True,null=True)
    
    def __str__(self):
        return self.cell
    

# Regulatory Compliance models
class RegulatoryCompliance(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
# Sustainability settingsm  Management Model
class SustainabilityManagent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    

# Admin Notification models
class Notification(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name