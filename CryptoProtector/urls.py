from django.urls import path, include
from . import views

urlpatterns = [
    path("",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("logout/",views.logout,name="logout"),
    path("share-file/",views.share_file,name="share-file"),
    path("received-files/",views.received_files,name="received-files"),
    path("received-files/<str:file_id>/",views.download_file,name="download-file"),
]
