from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
	path('', views.index, name = "index"),
	path('login', views.signin, name="signin"),
	path('logout', views.signout, name="signout"),
	path('registration', views.registration, name="registration"),
	path('artifact/<int:id>', views.get_artifact, name="artifact"),
	path('artifacts', views.get_artifacts, name="artifacts"),
	path('category/<int:id>', views.get_artifact_category, name="category"),
	path('writer/<int:id>', views.get_writer, name = "writer"),
]
