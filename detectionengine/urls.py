from django.urls import path
from .views import UploadFileView,GenerateReport


urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='upload-file'),
    path('results/', GenerateReport.as_view(), name='report')

]
