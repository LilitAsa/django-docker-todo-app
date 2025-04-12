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
    deadline = models.DateTimeField(null=True, blank=True)  # Optional deadline
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # Optional completion date
    
    # Flags for task status
    is_delayed = models.BooleanField(default=False)
    is_overdue = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)

    def check_flags(self):
        """
        This method checks if the task is overdue, delayed, urgent, or important
        based on certain conditions.
        """
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

    
    
