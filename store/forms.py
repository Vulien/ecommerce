from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'name', 'email', 'content']
        labels = {
            'rating': 'Đánh giá của bạn',
            'name': 'Họ và Tên',
            'email': 'Email',
            'content': 'Nhận xét',
        }
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
        }
