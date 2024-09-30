from django.urls import path
from .views import AddLanguageView, UpdateLanguageView, DeleteLanguageView

urlpatterns = [
    path("add/", AddLanguageView.as_view(), name="add_language"),
    path('update/<int:language_id>/', UpdateLanguageView.as_view(), name='update-language'),
    path('delete/<int:language_id>/', DeleteLanguageView.as_view(), name='delete-language'),
]
