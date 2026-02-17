from rest_framework import serializers
from .models import UserDetail
import secrets
import string



class UserDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ['unique_id'] 
    
    def generate_unique_id(self):
        characters = string.ascii_letters + string.digits
        while True:
            new_id = ''.join(secrets.choice(characters) for _ in range(10))
            if not UserDetail.objects.filter(unique_id=new_id).exists():
                return new_id

    def create(self, validated_data):
        validated_data['unique_id'] = self.generate_unique_id()
        return super().create(validated_data)    