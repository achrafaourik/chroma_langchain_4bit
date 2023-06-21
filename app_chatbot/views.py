from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json
from utils.huggingface_pipeline import HuggingFaceModel
from utils.instructor_embeddings import InstructorEmbeddings
from utils.emotion_pipeline import EmotionClassifier
from utils import functions
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import os
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
import numpy as np
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.views import View


class GoogleAuthCallbackView(View):
    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code', None)
        if auth_code is not None:
            # The authorization code is available as `auth_code`
            # You can now proceed to exchange it for an access token
            return HttpResponse(f"Authorization code: {auth_code}")
        else:
            # No code was provided
            return HttpResponse("No authorization code was provided.", status=400)


class GoogleAuthTokenView(View):
    def post(self, request, *args, **kwargs):
        auth_code = request.POST.get('code', None)
        if auth_code is None:
            return HttpResponseBadRequest("Missing authorization code.")

        data = {
            'code': auth_code,
            'client_id': '436766376383-rb4i7732u7fp14vae32th922t6cijv6j.apps.googleusercontent.com',
            'client_secret': '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',
            'redirect_uri': 'http://localhost:8000/oauth2callback',
            'grant_type': 'authorization_code',
        }

        response = requests.post('https://oauth2.googleapis.com/token', data=data)

        if response.status_code == 200:
            token_data = response.json()
            return JsonResponse(token_data)
        else:
            error_data = response.json()
            return JsonResponse({"error": "Failed to retrieve access token.", "details": error_data}, status=400)


class LoadModelsView(APIView):
    def get(self, request):
        # Create an instance of HuggingFaceModel
        huggingface_model = HuggingFaceModel()
        instructor_model = InstructorEmbeddings()
        emotion_model = EmotionClassifier()

        # Run the 'load' method
        huggingface_model.load()
        instructor_model.load()
        emotion_model.load()

        # You can perform further operations with the result if needed
        # For example, return it as a JSON response
        return Response({'message': 'Models successfully loaded'})


class ChatbotView(APIView):
    authentication_classes = [authentication.TokenAuthentication, OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        # Create instances of models
        huggingface_model = HuggingFaceModel()
        instructor_model = InstructorEmbeddings()
        emotion_model = EmotionClassifier()

        # Run the 'load' method
        huggingface_model.load()
        instructor_model.load()
        emotion_model.load()

        # # retrieve the user email from the incoming request
        # user = request.user
        email = "user2@email.com"

        # # get the body data from the request
        data = request.data
        text = data['message']

        # get related history
        related_history = functions.get_related_history(email, text)

        # # TODO: uncomment earlier lines later
        # history = ''

        # get the last n conversations
        past_conversations = functions.return_last_n_interactions(email,
                                                                  int(os.environ.get('N_RELATED_INTERACTIONS')))
        print(f'past 5 conversations of the client : {past_conversations}')

        # instantiate the model class and perform the prediction
        model = HuggingFaceModel()
        answer = model.predict(related_history, past_conversations, text)['answer']
        print(f"bot's answer: \n{answer}")

        # write the current interaction to ChromaDB
        current_interaction = "\n".join([f'USER: {text}', f'ASSISTANT: {answer}'])
        functions.write_current_interaction(email, current_interaction)

        # get the list of emotions
        # classifier = EmotionClassifier().get_classifier()
        # list_emotions = classifier(answer)
        # scores = [x['score'] for x in list_emotions[0]]
        # single_emotion = list_emotions[0][np.argmax(scores)]['label']

        # return Response({'answer': answer,
        #                  'list_emotions': list_emotions,
        #                  'single_emotion': single_emotion})

        return Response({'answer': answer})


class CatbotView(APIView):

    def post(self, request):

        # # retrieve the user email from the incoming request
        user = request.user
        email = request.email

        # # get the body data from the request
        data = request.data
        text = data['message']

        # # get related history
        history = functions.get_related_history(email, text)

        # instantiate the model class and perform the prediction
        model = HuggingFaceModel()
        answer = model.predict(history, text)['answer']
        print(f"bot's answer: \n{answer}")

        # write the current interaction to ChromaDB
        current_interaction = "\n".join([f'USER: {text}', f'ASSISTANT: {answer}'])
        functions.write_current_interaction(email, current_interaction)

        return Response({'answer': answer})
