from django.urls import path
from . import views

urlpatterns = [
    path('', views.NLPView.as_view(), name="nlp"),
    path('api', views.KoboldAIView.as_view(), name="kobold"),
    path('kobold', views.WebAppView, name="kobold_ui") # kobald url
]
