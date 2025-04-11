from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def average_rating(self):
        ratings = self.ratings.all().aggregate(models.Avg('value'))['value__avg']
        return ratings or 0

    def similar_projects(self):
        # Get projects with similar tags
        return Project.objects.filter(
            tags__in=self.tags.all()
        ).exclude(id=self.id).distinct()[:4]

    def is_cancelable(self):
        total_donations = self.donations.aggregate(models.Sum('amount'))['amount__sum'] or 0
        return total_donations < (0.25 * self.total_target)

    @property
    def aggregate_total_amount(self):
        """إجمالي التبرعات للمشروع"""
        return self.donations.aggregate(models.Sum('amount'))['amount__sum'] or 0

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f"Image for {self.project.title}"

    class Meta:
        ordering = ['id']  # Ensure consistent ordering of images


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅
    project = models.ForeignKey(Project, related_name='donations', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} donated {self.amount} to {self.project.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username if self.user else 'Anonymous'} on {self.project.title}"


class ProjectReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='reports', on_delete=models.CASCADE)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reported {self.project.title}"


class CommentReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='reports', on_delete=models.CASCADE)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reported a comment"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ كده يقبل التقييم من غير مستخدم
    project = models.ForeignKey(Project, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    rated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} rated {self.project.title} with {self.value}"


class CancelledProject(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project {self.project.title} was cancelled"


def cancel_project_if_needed(project):
    """إلغاء المشروع إذا لم تصل التبرعات إلى 25٪ من الهدف."""
    if project.is_cancelable():
        CancelledProject.objects.create(
            project=project,
            cancelled_by=project.creator,
            reason="Donations did not reach 25% of the target."
        )
