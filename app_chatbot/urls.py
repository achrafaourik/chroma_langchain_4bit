from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatbotView.as_view(), name="nlp"),
    path('load/', views.LoadModelsView.as_view(), name='huggingface'),
    path('oauth2callback', GoogleAuthCallbackView.as_view(), name='auth_view'),  # The GoogleAuthCallbackView handles the redirection from Google

]
