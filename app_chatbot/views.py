from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json
from utils.huggingface_pipeline import HuggingFaceModel
from django.http import HttpResponse
import os
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken


class ChatbotView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user  # TODO: replace with self.request.user

        email = user.email

