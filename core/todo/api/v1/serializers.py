from ...models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['author','title','status','created_date','updated_date']
        
        

        
        

