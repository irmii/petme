from rest_framework import serializers
from .models import TypeOfPet

class PetSerializer(serializers.ModelSerializer):
    type_breeds = serializers.StringRelatedField(many=True)

    class Meta:
        model = TypeOfPet
        fields = ['type', 'type_breeds']