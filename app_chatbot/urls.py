from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatbotView.as_view(), name="nlp"),
    path('load/', LoadModelsView.as_view(), name='huggingface')
]
