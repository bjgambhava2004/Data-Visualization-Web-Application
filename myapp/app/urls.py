from django.urls import path
from .views import upload_csv, sales_chart

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('sales-chart/', sales_chart, name='sales_chart'),
]
