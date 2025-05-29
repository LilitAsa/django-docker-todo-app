from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name="userprofile"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
      
      
class Task(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True) 
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False, null=True, blank=True)
    is_delayed = models.BooleanField(default=False, null=True, blank=True)
    is_overdue = models.BooleanField(default=False, null=True, blank=True)
    is_urgent = models.BooleanField(default=False, null=True, blank=True)
    is_important = models.BooleanField(default=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_archived = models.BooleanField(default=False, null=True, blank=True)
    is_favorite = models.BooleanField(default=False, null=True, blank=True)

    def check_flags(self):
        """
        This method checks if the task is overdue, delayed, urgent, or important
        based on certain conditions.
        """
        # Only save if the user_profile is set
        if self.user_profile_id is not None:
            now = timezone.now()

            # Set is_overdue if the task's deadline has passed
            if self.deadline and self.deadline < now:
                self.is_overdue = True

            # Set is_delayed if the task's deadline is in the future but it's not completed
            # (you can implement completion logic based on your model)
            elif self.deadline and self.deadline > now:
                self.is_delayed = True

            # Set is_urgent based on your own logic (e.g., if it's within 24 hours)
            if self.deadline and self.deadline <= now + timezone.timedelta(hours=24):
                self.is_urgent = True

            # Mark is_important based on some condition, for example, tasks marked by users as important
            if self.title.lower() in ['critical', 'important', 'high priority']:  # Example condition
                self.is_important = True

            self.save()

    def __str__(self):
        return self.title

    
    
