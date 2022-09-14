from django.urls import path
from nfc.views import IndexView
from nfc.views import Validate
from nfc.views import Error

urlpatterns = [
    path('<slug:uid>/<slug:sn>/', IndexView.as_view()),
    path('validate', Validate.as_view()),
    path('', Error.as_view() ),
]