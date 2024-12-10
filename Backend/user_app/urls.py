from django.urls import path
from .views import Sign_Up, Log_in, Log_out

app_name = "user_app"
urlpatterns = [
    # POST Create a user
    path("signup/", Sign_Up.as_view(), name="signup"),
    # POST An existing user signs in
    path("login/", Log_in.as_view(), name="login"),
    # POST A user signs out
    path("logout/", Log_out.as_view(), name="logout"),
]
