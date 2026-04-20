from django.urls import path
from .views import GetSingleUserView, UserClassificationView

urlpatterns = [
    path('profiles', UserClassificationView.as_view(), name='user-classification'),
    path('profiles/<str:user_id>', GetSingleUserView.as_view(), name='get-single-user'),
]