from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index),
    path('login_page', views.login_page),
    path("register_page", views.register_page),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path("my_recipes", views.my_recipes),
    path("all_recipes", views.all_recipes),
    path("category_recipes/<str:category_name>", views.category_recipes),
    path("add_recipe_page", views.add_recipe_page),
    path("recipe_details/<int:recipe_id>", views.recipe_details),
    path("add_recipe", views.add_recipe),
    path('write_review/<int:recipe_id>', views.write_review),
    path('search', views.search),
    path('delete_review/<int:review_id>', views.delete_review)

]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
