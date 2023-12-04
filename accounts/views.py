from rest_framework.views import APIView
from rest_framework.response import Response
from .srializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



class UserRegistration(APIView):
    def post(self, request):
        user_serializer = UserRegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
        return Response(data=user_serializer.errors)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.username}!'},
            status=status.HTTP_204_NO_CONTENT
        )

