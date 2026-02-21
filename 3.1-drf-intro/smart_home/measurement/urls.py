from django.urls import path

from measurement.views import SensorLiCrView, SensorRetUpView, MeasCrView

urlpatterns = [
    path('sensor/', SensorLiCrView.as_view()),
    path('sensor/<pk>/', SensorRetUpView.as_view()),
    path('measurements/', MeasCrView.as_view()),
]
