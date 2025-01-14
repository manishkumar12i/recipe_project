from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('receipes/',views.receipes,name="receipes"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('register/',views.register_user,name="register"),
    path('update_receipes/<r_id>/',views.update_receipe,name="update_receipes"),
    path('delete_receipes/<r_id>/',views.delete_receipe,name="delete_receipes")
]