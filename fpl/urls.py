from django.urls import path
from .views import *

urlpatterns = [
    path('general-info/', FetchFPLGeneralInfoView.as_view(), name='fpl-general-info'),
    path('fixtures/', FetchFPLFixturesView.as_view(), name='fpl-fixtures'),
    path('player/<int:player_id>/', PlayerDetailView.as_view(), name='fpl-player-detail'),
    path('player/<str:opta_code>/', PlayerPhotoView.as_view(), name='fpl-player-photo'),
    path('gameweek/<int:event_id>/live/', LiveGameweekDataView.as_view(), name='fpl-gameweek-live'),
    path('team/<int:team_id>/', FetchFPLTeamView.as_view(), name='fpl-team'),
    path('team/<int:team_id>/history/', FetchFPLTeamHistoryView.as_view(), name='fpl-team-history'),
    path('team/<int:team_id>/transfers/', FetchFPLTransfersView.as_view(), name='fpl-team-transfers'),
    path('team/<int:team_id>/event/<int:gw>/picks/', FetchFullTeamDetailsView.as_view(), name='fpl-team-picks'),
    path('league/classic/<int:page>/<int:leagueId>/', FetchFPLLeagueView.as_view(), name='fpl-classic-league'),
    path('league/h2h/<int:leagueId>/', FetchFPLH2HLeagueView.as_view(), name='fpl-h2h-league'),
]