
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
#router.register('LoanApi', views.ApprovalsView)
urlpatterns = [
    path('api/', include(router.urls)),
   # path('status/', views.predictor),
    path('form/', views.loanform, name='LoanForm'),
] 