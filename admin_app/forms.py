from django import forms
from .models import Crop,CropFertilizerPredict,RegulatoryCompliance,SustainabilityManagent

# Crops Form
class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ('crop_image','crop_name', 'description', 'planting_time', 'fertilizer', 'irrigation','harvest', 'cleaning','storage',
                  'transportation','consumption','end_of_life')

# Crop Prediction Form
class CropPredictForm(forms.ModelForm):
    class Meta:
        model = CropFertilizerPredict
        fields = ('cell', 'nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall', 'temperature',)


# Regulatory Compliance
class RegulatoryComplianceForm(forms.ModelForm):
    class Meta:
        model = RegulatoryCompliance
        fields = ('title', 'description',)

# Sustainability Management
class SustainabilityManagentForm(forms.ModelForm):
    class Meta:
        model = SustainabilityManagent
        fields = ('title', 'description',)
