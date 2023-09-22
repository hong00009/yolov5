from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import UserProfile
from django import forms

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
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = UserProfile
        fields = ['gender', 'birthdate', 'height', 'weight']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date', 'value': '2000-01-01'}),
        }