from django.urls import path
from home import views

urlpatterns = [
    path("",views.index,name="homepage"),
    path("friend/<str:pk>/",views.friend,name="friend"),
    path("friends/",views.all_friend,name="friends"),
    path("logout/",views.logout_user,name="logout"),
    path("sent_msg/<str:pk>/",views.sentMessage,name="sent_msg"),
    path("receive_msg/<str:pk>/",views.recerivedMessges,name="receive_msg"),
    path("profile/<str:pk>/",views.profile_page,name="profile"),
    path("edit/<str:pk>/",views.edit_profile,name="edit"),
    path('get_unseen_message_count/<int:friend_id>/', views.get_unseen_message_count, name='get_unseen_message_count'),
    path("register/",views.signup_user,name="register"),
    path("login/",views.login_user,name="login")
]

