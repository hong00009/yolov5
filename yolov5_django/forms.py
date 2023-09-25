from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image']


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image']

    title = forms.CharField(required=True)  # 선택적으로 제목 수정 가능하도록
    image = forms.ImageField(required=True)  # 선택적으로 이미지 수정 가능하도록


class DateRangeFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.TextInput(attrs={'type': 'date'}))
