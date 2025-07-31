from django.db import models

# Create Task model:
class Task (models.Model):
    author = models.ForeignKey('accounts.Profile',on_delete=models.CASCADE)
    title = models.CharField(max_length=250) 
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
