from django import forms
from .models import Post
from django.utils import timezone
from datetime import datetime, timedelta
from django.forms import DateInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content', 'image', 'post_time', 'hour']
        labels = {
            'title': '제목',
            'image': '이미지',
        }

    text_content = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}),
        )    

    post_time = forms.DateField(
        initial=timezone.now().date(), # timezone-aware 형태로 수정
        # initial=datetime.now().date(),
        widget=DateInput(attrs={'type': 'date'}),
        label='날짜',
    )
    # 시간 선택 범위 설정
    HOUR_CHOICES = [(str(hour), str(hour)) for hour in range(24)]
    
    hour = forms.ChoiceField(choices=HOUR_CHOICES, label='시간')

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'accept':'image/*'}),
    )
    
    def clean(self):
        cleaned_data = super().clean()
        post_time = cleaned_data.get('post_time')
        hour = cleaned_data.get('hour')

        if post_time is not None and hour is not None:
            try: # post_time의 0시0분0초값 + hour값
                post_time = datetime.combine(post_time, datetime.min.time()) + timedelta(hours=int(hour))
                post_time = timezone.make_aware(post_time) # timezone-aware 형태로 변환
            except ValueError:
                raise forms.ValidationError('Invalid date or time')

            cleaned_data['post_time'] = post_time

        return cleaned_data


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_content', 'post_time', 'hour']

    title = forms.CharField(required=True)
    text_content = forms.CharField(required=True)
    post_time = forms.DateTimeField(required=True)

    HOUR_CHOICES = [(str(hour), str(hour)) for hour in range(24)]
    hour = forms.ChoiceField(choices=HOUR_CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        post_time = cleaned_data.get('post_time')
        hour = cleaned_data.get('hour')

        if post_time is not None and hour is not None:
            try: # post_time의 0시0분0초값 + hour값
                date_hour = datetime.combine(post_time, datetime.min.time()) + timedelta(hours=int(hour))
                post_time = timezone.make_aware(date_hour) # timezone-aware 형태로 변환
            except ValueError:
                raise forms.ValidationError('Invalid date or time')

            cleaned_data['post_time'] = post_time

        return cleaned_data


class DateRangeFilterForm(forms.Form):
    start_date = forms.DateField(
        label='시작 날짜',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date', 'value': timezone.now().date(), 'class': 'custom-date-input'})
    )
    end_date = forms.DateField(
        label='마지막 날짜',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date', 'value': timezone.now().date(), 'class': 'custom-date-input'})
    )
