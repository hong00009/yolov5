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


class DropdownFrom(forms.Form):
    widget=forms.Select(choices=3)
    