from django.urls import path
from . import views

app_name = 'gastos'

urlpatterns = [
    path('', views.lista_gastos, name='lista'),
    path('criar/', views.criar_gasto, name='criar'),
    path('<int:pk>/editar/', views.editar_gasto, name='editar'),
    path('<int:pk>/deletar/', views.deletar_gasto, name='deletar'),
    path('<int:pk>/deletar-htmx/', views.deletar_gasto_htmx, name='deletar_htmx'),  # NOVO
    path('<int:pk>/marcar-pago/', views.marcar_pago, name='marcar_pago'),
]
