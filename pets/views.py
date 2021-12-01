from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PetSerializer
from .models import TypeOfPet
from .pet_url_switcher import PetUrlSwitcher

class BreedsAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            pet_request = request.GET.get('pet', '')
            pet_type = PetUrlSwitcher.switch(pet_request)

            breeds = TypeOfPet.objects.get(type=pet_type)

            serializer = PetSerializer(breeds)
            formatted_data = serializer.data['type_breeds']
            return Response(formatted_data)
        except TypeOfPet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)