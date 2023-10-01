from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

from .models import UserProfile, UserFoodNutritions, FoodNutrition

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # UCF 상속, model만 내것으로수정하고 나머지 그대로
        model = get_user_model()
        fields = ('username', )
        

class CustomAuthenticationForm(AuthenticationForm):
    pass

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)

        
class UserProfileForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('male', '남성'),
        ('female', '여성'),
    )
    
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'inline-radio'}))
    gender.label = '성별'
    
    class Meta:
        model = UserProfile
        fields = ['gender', 'birthdate', 'height', 'weight']
        
        labels = {
        'birthdate': '생년월일',
        'weight': '체중 (kg)',
        'height': '키 (cm)',
        }
        
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date', 
                                                'value': '2000-01-01'}),
        }

class UserNutritionsEditForm(forms.ModelForm):
    nutrition_info = forms.ModelChoiceField(queryset=FoodNutrition.objects.all(), label='')
    delete = forms.BooleanField(required=False, label='삭제')

    class Meta:
        model = UserFoodNutritions
        fields = ['nutrition_info', 'delete']