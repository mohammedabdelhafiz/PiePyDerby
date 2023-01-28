from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_login_regi),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('add/pie', views.add_pie),
    path('edit/<int:id>', views.render_edit_pie),
    path('edit/pie', views.edit_pie),
    path('delete/<int:id>', views.delete_pie),
    path('pies', views.pies_show),
    path('show/<int:id>', views.pie_show),
    path('vote/<int:id>', views.vote),
    path('unvote/<int:id>', views.unvote),
]