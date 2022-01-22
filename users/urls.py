from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('make_ca/', views.make_ca, name='make_ca'),
    # path('join_team/', join_team, name='join_team'),
    path('create_team/<int:eventid>/', views.create_team, name='create_team'),
    path('join_team/', views.join_team, name='join_team'),
    path('edit_team/<slug:teamid>/', views.edit_team, name='edit_team'),
    path('delete_team/<slug:teamid>/', views.delete_team, name='delete_team'),
    # path('team_created/<slug:teamid>/', team_created, name='team_created'),
    # path('join_team/confirm/', join_team_confirm, name='join_team_confirm'),
    # path('profile/', user_profile, name='user_profile'),
    # path('profile/update/', update_profile, name='update_profile'),
    # path('profile/ambassador/', make_ambassador, name="make_ambassador"),
    # path('profile/edit_team/<slug:teamid>/', edit_team, name='edit_team'),
]
