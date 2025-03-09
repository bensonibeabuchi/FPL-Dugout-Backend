from django.urls import path
from .views import *

urlpatterns = [
    path('general-info/', FetchFPLGeneralInfoView.as_view(), name='fpl-general-info'),
    path('fixtures/', FetchFPLFixturesView.as_view(), name='fpl-fixtures'),
    path('player/<int:player_id>/', PlayerDetailView.as_view(), name='fpl-player-detail'),
    path('player/<str:opta_code>/', PlayerPhotoView.as_view(), name='fpl-player-photo'),
    path('gameweek/<int:event_id>/live/', LiveGameweekDataView.as_view(), name='fpl-gameweek-live'),
    path('team/<int:teamId>/', FetchFPLTeamView.as_view(), name='fpl-team'),
    path('team/<int:teamId>/history/', FetchFPLTeamHistoryView.as_view(), name='fpl-team-history'),
    path('team/<int:teamId>/transfers/', FetchFPLTransfersView.as_view(), name='fpl-team-transfers'),
    path('team/<int:teamId>/event/<int:gw>/picks/', FetchFullTeamDetailsView.as_view(), name='fpl-team-picks'),
    path('league/classic/<int:leagueId>/', FetchFPLLeagueView.as_view(), name='fpl-classic-league'),
    path('league/h2h/<int:leagueId>/', FetchFPLH2HLeagueView.as_view(), name='fpl-h2h-league'),
    path('event-status/', EventStatusView.as_view(), name='event-status'),
    path('players/<int:leagueId>/<int:gw>/', get_players, name='get_players'),
    path('team/<int:teamId>/<int:gw>/points/', FetchTeamEventPointsView.as_view(), name='fetch_team_event_points'),
    path('team/<int:teamId>/<int:gw>/live-total-points/', FetchTeamLiveTotalPointsView.as_view(), name='fetch_team_live_total_points'),
    path('league/<int:leagueId>/live-points/', FetchLeagueLiveTotalPointsView.as_view(), name='fetch_league_live_total_points'),


]