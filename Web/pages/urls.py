from .views.others import (
    home,
    about,
    chat,
    code_edit_python,
    code_edit_javascript,
    code_view,
    solve_task,
    task_description,
    lesson_components,
    course_communications
)
from django.urls import path
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('code_edit/python/', code_edit_python, name='code_edit_python'),
    path('code_edit/javascript/', code_edit_javascript, name='code_edit_javascript'),
    path('view_code_snippet/', code_view, name='view_code_snippet'),
    path('solve_task/', solve_task, name='solve_task'),
    path('solve_task/', solve_task, name='solve_task'),
    path('chat/<int:course_id>/<str:auth_token>/', chat, name='chat'),
    path('task_description/<int:task_id>/<str:auth_token>/', task_description, name='task_description'),
    path('lesson_components/<int:lesson_id>/<str:auth_token>/', lesson_components, name='lesson_component'),
    path('course_communications/<int:course_id>/<str:auth_token>/', course_communications, name='course_communications')
]
from .views import dashboard
# Dashboard Urls
urlpatterns += [
    path("dashboard/", view=dashboard.dashboard_view, name="dashboard"),
    path("dashboard/courses", view=dashboard.dashboard_view, name="courses"),
    path("dashboard/teachers", view=dashboard.dashboard_view, name="teachers"),
    path("dashboard/students", view=dashboard.dashboard_view, name="students"),
    path("dashboard/settings", view=dashboard.dashboard_view, name="settings"),
    path("dashboard/logout", view=dashboard.dashboard_view, name="logout"),
]
