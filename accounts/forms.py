from django import forms
from django.contrib.auth.models import User
from .models import UserProfiles

# This is user form
class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

# This is User profile form
class UserProfileForm(forms.ModelForm):
    title = forms.CharField(disabled=True)
    province = forms.CharField(disabled=True)
    district = forms.CharField(disabled=True)
    sector = forms.CharField(disabled=True)
    
    class Meta:
        model = UserProfiles
        fields = ['photo','title','province','district','sector','cell']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['photo'].widget.attrs.update({'class':'image_upload'})
        

# Helper for dashboard access
class UserTitleForm(forms.ModelForm):
    class Meta:
        model = UserProfiles
        fields = ('title',)