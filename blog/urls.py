from django.urls import path
from . import views
from .views import PostListView,PostDetailView, SubjectView
from .views import emailView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('about/', views.about, name='blog-about'),
    path('iletisim/', emailView, name='blog-email'),
    path('<str>/', SubjectView.as_view(), name='post-subject'),
    

]
