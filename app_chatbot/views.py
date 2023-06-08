from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json
from utils.huggingface_pipeline import HuggingFaceModel
from uitls.instructor_embeddings import InstructorEmbeddings
from utils import functions
from django.http import HttpResponse
import os
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken


class LoadModelsView(APIView):
    def get(self, request):
        # Create an instance of HuggingFaceModel
        huggingface_model = HuggingFaceModel()
        instructor_model = InstructorEmbeddings()

        # Run the 'load' method
        huggingface_model.load()
        instructor_model.load()

        # You can perform further operations with the result if needed
        # For example, return it as a JSON response
        return Response({'message': 'Models successfully loaded'})


class ChatbotView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        # retrieve the user email from the incoming request
        user = request.user
        email = user.email

        # get the body data from the request
        data = request.data
        text = data['message']

        # get related history
        history = functions.get_related_history(email, text)

        # instantiate the model class and perform the prediction
        model = HuggingFaceModel()
        answer = model.predict(history, text)['answer']
        print(f"bot's answer: \n{answer}")

        # write the current interaction to ChromaDB
        current_interaction = "\n".join([f'USER: {text}', f'ASSISTANT: {answer}'])

        functions.write_current_interaction(email, current_interaction)

        return Response(answer)
