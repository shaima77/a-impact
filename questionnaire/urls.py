from django.urls import path
from . import views

app_name = 'questionnaire'

urlpatterns = [
    path('', views.home, name='home'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('submit/', views.submit_assessment, name='submit_assessment'),
    path('report/<int:report_id>/', views.view_report, name='view_report'),
    path('api/requirements/', views.api_get_requirements, name='api_requirements'),
]
