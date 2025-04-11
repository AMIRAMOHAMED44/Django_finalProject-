from django import forms
from .models import Donation, Rating, Project, Comment, ProjectImage
from django.shortcuts import render, redirect
from django.contrib import messages

# نموذج إضافة مشروع
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'total_target': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


# نموذج صور المشروع (يدعم رفع أكثر من صورة)
class ProjectImageForm(forms.Form):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Project Images'
    )


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
