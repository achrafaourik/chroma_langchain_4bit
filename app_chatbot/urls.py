from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatbotView.as_view(), name="nlp"),
    path('load/', views.LoadModelsView.as_view(), name='huggingface'),
    path('delete_hist/', views.DeleteHistoryView.as_view(), name='huggingface'),
    path('oauth2callback', views.GoogleAuthCallbackView.as_view(), name='auth_view'),
    path('getauthtoken', views.GoogleAuthTokenView.as_view(), name='token_view'),
]
