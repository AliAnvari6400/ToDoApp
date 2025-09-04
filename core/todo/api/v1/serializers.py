from ...models import Task
from accounts.models import Profile
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url',read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name = 'get_absolute_url')
    
    class Meta:
        model = Task
        fields = ['author','title','snippet','relative_url','absolute_url','status','created_date','updated_date']
        read_only_fields = ['author']
        
    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self,instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        rep['state'] = 'list'
        #print(request.__dict__)
        if request.parser_context.get('kwargs').get('pk'):
            rep['state'] = 'single'
            rep.pop('snippet',None)
            rep.pop('relative_url',None)
            rep.pop('absolute_url',None)
        # else:
        #     rep.pop('status',None)
        return rep
    
    def create(self,validated_data):
        validated_data['author'] = Profile.objects.get(user=self.context.get('request').user.id)
        return super().create(validated_data)
