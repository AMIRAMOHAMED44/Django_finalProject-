from django import forms
from .models import Donation, Rating, Project, Comment, ProjectImage


# نموذج إضافة مشروع
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time', 'tags']


# نموذج صورة المشروع (يقبل صورة واحدة فقط)
class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput()  # لا داعي للـ multiple هنا
        }



# نموذج التبرع
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

# نموذج التقييم
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.Select(attrs={'class': 'form-control'}, choices=[(i, i) for i in range(1, 6)]),
        }

# نموذج التعليقات
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # حقل النص فقط في التعليق
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
