from django.forms import ModelForm
from django import forms
from .models import Review,Post

class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=['asin',
                    'page_number',
                    'review_text',
                    'pub_date',
                    'review_header',
                    'review_rating',
                    'review_author']

class ScrapeForm(forms.Form):

    asin = forms.CharField(max_length=30, label='name')
    widgets = {
        'title': forms.TextInput(),
    }

class ProductListForm(forms.Form):
    keywords = forms.CharField(max_length=30, label='name')
    widgets = {
        'title': forms.TextInput(),
    }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # exclude = ['author', 'updated', 'created', ]
        fields = ['text']
        widgets = {
            'text': forms.TextInput(
                attrs={'style': 'width:700px','id': 'post-text', 'required': True, 'placeholder': 'Say something...'}
            ),
        }


from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password'] # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.
