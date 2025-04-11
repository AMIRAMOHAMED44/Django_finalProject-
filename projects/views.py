from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib import messages
from .models import Project, Comment, Rating, ProjectImage, Tag
from .forms import CommentForm, DonationForm, RatingForm, ProjectForm, ProjectImageForm
from .models import Project, Category
from django.core.exceptions import ValidationError


def project_list(request):
    projects = Project.objects.all().order_by('-created_at').prefetch_related('images', 'tags')
    tags = Tag.objects.all()
    
    # Filter by tag if specified
    selected_tag = request.GET.get('tag')
    if selected_tag:
        projects = projects.filter(tags__name=selected_tag)
    
    # Calculate total donations for each project
    for project in projects:
        project.total_donations = project.donations.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        project.progress_percentage = (project.total_donations / project.total_target * 100) if project.total_target > 0 else 0
        print(f"Project {project.title} has {project.images.count()} images")  # Debug print
    
    context = {
        'projects': projects,
        'tags': tags,
        'selected_tag': selected_tag
    }
    return render(request, 'project_list.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project.objects.prefetch_related('images'), id=project_id)
    donation_form = DonationForm(request.POST or None)
    comment_form = CommentForm(request.POST or None)
    rating_form = RatingForm(request.POST or None)

    # Calculate total donations
    total_donations = project.donations.aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    progress_percentage = (total_donations / project.total_target * 100) if project.total_target > 0 else 0

    user_rating = project.ratings.filter(user=request.user).first() if request.user.is_authenticated else None

    if request.method == 'POST':
        if 'donate' in request.POST and donation_form.is_valid():
            donation = donation_form.save(commit=False)
            donation.user = request.user if request.user.is_authenticated else None
            donation.project = project
            donation.save()
            messages.success(request, 'Thanks for your donation!')
            return redirect('project_detail', project_id=project.id)

        elif 'comment' in request.POST and comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.project = project
            comment.user = request.user if request.user.is_authenticated else None
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('project_detail', project_id=project.id)

        elif 'rate' in request.POST and rating_form.is_valid():
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
        'progress_percentage': progress_percentage,
        'user_rating': user_rating,
    }
    return render(request, 'project_detail.html', context)

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        
        if form.is_valid():
            # Save the basic project info
            project = form.save(commit=False)
            project.creator = request.user
            try:
                project.save()
                form.save_m2m()  # Save many-to-many relationships (e.g., tags)

                # Handle image uploads
                images = request.FILES.getlist('images')
                for image in images:
                    if image.content_type not in ['image/jpeg', 'image/png']:
                        raise ValidationError("Only JPEG and PNG images are allowed.")
                    if image.size > 5 * 1024 * 1024:  # 5 MB limit
                        raise ValidationError("Each image must be less than 5 MB.")
                    ProjectImage.objects.create(project=project, image=image)

                messages.success(request, 'Project created successfully!')
                return redirect('project_detail', project_id=project.id)
            except ValidationError as e:
                messages.error(request, f'File upload error: {e}')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {str(e)}')
                print(f"Error: {e}")  # Log the error for debugging
        else:
            messages.error(request, 'Please fix the errors below.')
            print("Form errors:", form.errors)  # Log form errors for debugging
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})

from django.shortcuts import render
from .models import Project, Category

def home(request):
    top_rated_projects = Project.objects.annotate(
        avg_rating=models.Avg('ratings__value')
    ).order_by('-avg_rating')[:5]
    
    latest_projects = Project.objects.order_by('-created_at')[:5]
    
    featured_projects = Project.objects.filter(
        total_target__gte=10000  
    )[:5]
    
    categories = Category.objects.all()
    
    context = {
        'top_rated_projects': top_rated_projects,
        'latest_projects': latest_projects,
        'featured_projects': featured_projects,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def category_projects(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    projects = Project.objects.filter(category=category)
    return render(request, 'projects/category.html', {
        'category': category,
        'projects': projects
    })