from django import forms
from .models import UploadedImage

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']


class EditImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']

    title = forms.CharField(required=True)  # 선택적으로 제목 수정 가능하도록
    image = forms.ImageField(required=True)  # 선택적으로 이미지 수정 가능하도록


class DateRangeFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.TextInput(attrs={'type': 'date'}))
