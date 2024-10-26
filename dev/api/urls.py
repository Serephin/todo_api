from django.urls import path
from . import views




urlpatterns=[
    path('all', views.UserToDoListView.as_view(),name='all-tasks'),
    path('<int:pk>',views.TaskDetailSerealizerView.as_view(), name='todo-detail'),
    path('create',views.CreateToDoView.as_view()),
    path('<int:pk>/update/', views.UpdateToDoView.as_view(), name='todo-update'),
    path('<int:pk>/delete/', views.DeleteToDoView.as_view(), name='todo-delete'),]