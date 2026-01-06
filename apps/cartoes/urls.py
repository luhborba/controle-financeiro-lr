from django.urls import path

app_name = 'cartoes'

urlpatterns = [
    # Vamos criar as views depois
    path('', lambda r: None, name='lista'),
]
