from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib import messages
from .models import Project, Comment, Rating, ProjectImage
from .forms import CommentForm, DonationForm, RatingForm, ProjectForm, ProjectImageForm

def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    donation_form = DonationForm(request.POST or None)
    comment_form = CommentForm(request.POST or None)
    rating_form = RatingForm(request.POST or None)

    total_donations = project.donations.aggregate(models.Sum('amount'))['amount__sum'] or 0
    user_rating = project.ratings.filter(user=request.user).first() if request.user.is_authenticated else None

    if request.method == 'POST':
        if 'donate' in request.POST:
            if donation_form.is_valid():
                donation = donation_form.save(commit=False)
                donation.user = request.user if request.user.is_authenticated else None
                donation.project = project
                donation.save()
                messages.success(request, 'Thanks for your donation!')
                return redirect('project_detail', project_id=project.id)
        elif 'comment' in request.POST:
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.project = project
                comment.user = request.user if request.user.is_authenticated else None
                comment.save()
                messages.success(request, 'Your comment has been added!')
                return redirect('project_detail', project_id=project.id)
        elif 'rate' in request.POST:
            if rating_form.is_valid():
                rating_value = rating_form.cleaned_data['value']
                if not user_rating:
                    user = request.user if request.user.is_authenticated else None
                    Rating.objects.create(project=project, user=user, value=rating_value)
                    messages.success(request, 'Thanks for your rating!')
                    return redirect('project_detail', project_id=project.id)

    context = {
        'project': project,
        'donation_form': donation_form,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'total_donations': total_donations,
        'user_rating': user_rating,
    }
    return render(request, 'project_detail.html', context)


# def create_project(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST, request.FILES)
#         image_form = ProjectImageForm(request.POST, request.FILES)
#
#         # التحقق من صلاحية النموذج الخاص بالمشروع
#         if form.is_valid():
#             # حفظ المشروع
#             project = form.save(commit=False)
#             project.save()
#
#             # إضافة الصورة المرتبطة بالمشروع إذا تم رفعها
#             if image_form.is_valid() and image_form.cleaned_data.get('image'):
#                 ProjectImage.objects.create(project=project, image=image_form.cleaned_data['image'])
#
#             # التوجيه إلى صفحة عرض قائمة المشاريع بعد الحفظ
#             return redirect('project_list')  # تأكد من وجود URL باسم 'project_list'
#
#         else:
#             # طباعة الأخطاء لتشخيص المشكلة
#             print("Form errors:", form.errors)
#
#             # عرض الأخطاء في واجهة المستخدم
#             return render(request, 'create_project.html', {'form': form, 'image_form': image_form})
#
#     else:
#         form = ProjectForm()
#         image_form = ProjectImageForm()
#
#     return render(request, 'create_project.html', {'form': form, 'image_form': image_form})
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        image_form = ProjectImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            # حفظ المشروع
            project = form.save(commit=False)
            project.creator = request.user if request.user.is_authenticated else None
            project.save()
            form.save_m2m()

            # حفظ الصورة إن وجدت
            image = image_form.cleaned_data.get('image')
            if image:
                ProjectImage.objects.create(project=project, image=image)

            return redirect('project_list')  # تأكد إن عندك URL اسمه كده
        else:
            print("Form errors:", form.errors)
            print("Image form errors:", image_form.errors)

    else:
        form = ProjectForm()
        image_form = ProjectImageForm()

    return render(request, 'create_project.html', {
        'form': form,
        'image_form': image_form
    })


# def search_projects(request):
#     query = request.GET.get('q')
#     projects = Project.objects.filter(title__icontains(query) if query else Project.objects.all())
#     return render(request, 'search_results.html', {'projects': projects})
