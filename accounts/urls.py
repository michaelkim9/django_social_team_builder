from django.conf.urls import url

from . import views

app_name = "accounts"

urlpatterns = [
    url(r"login/$", views.LoginView.as_view(), name="login"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
    url(r"logout/$", views.LogoutView.as_view(), name="logout"),
    url(r"^profile/(?P<username>[a-zA-Z0-9_]+)$",
        views.ProfileView.as_view(),
        name='profile'),
    url(r"^profile/(?P<username>[a-zA-Z0-9_]+)/edit/$", views.EditProfileView.as_view(), name="edit_profile"),
    url(r'^user/applications/$', views.UserApplications.as_view(), name='my_applications'),
    url(r'^user/applications/(?P<position>\d+)/(?P<applicant>\d+)/(?P<status>\w+)/$',
        views.UserApplicationStatus.as_view(), name='status_update'),
    url(r'^user/notifications/$', views.UserNotifications.as_view(), name='my_notifications'),
]
