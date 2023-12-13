from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendors/',views.vendorViews.as_view()),
    path('vendors/<id>/',views.vendorViews.as_view()),
    path('purchase_orders/',views.PoViews.as_view()),
    path('purchase_orders/<id>/',views.PoViews.as_view()),
    path('vendor/<id>/performance/',views.Performance.as_view()),
]
