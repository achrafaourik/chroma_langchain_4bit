from django.urls import path
from . import views

urlpatterns = [
    path('hf/', views.ChatbotView.as_view(), name="hf"),
    path('load/', views.LoadModelsView.as_view(), name='load_hf'),
    path('ooba/', views.OoobaView.as_view(), name='oobabooga'),
    path('delete_hist/', views.DeleteHistoryView.as_view(), name='delete_history'),
    path('oauth2callback', views.GoogleAuthCallbackView.as_view(), name='auth_view'),
    path('getauthtoken', views.GoogleAuthTokenView.as_view(), name='token_view'),
]
