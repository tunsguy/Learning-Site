from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("room/<str:pk>", views.room, name="room"),
    path("create-room/",views.createRoom,name="create"),
    path("update-room/<str:pk>",views.updateRoom,name="update"),
    path("delete-room/<str:pk>",views.deleteRoom,name="delete"),
    path("login/",views.loginPage,name="login"),
    path("logout/",views.logoutPage,name="logout"),
    path("register/",views.registerPage,name="register"),
    path("delete-message/<str:pk>",views.deletemessage,name="deletemessage"),
    path("profile/<str:pk>",views.profile,name="profile"),
    path("update-user/",views.UpdateUser,name="update-user"),
    path("activity/",views.activity,name="activity"),
    path("topics/",views.topics,name="topics"),
]