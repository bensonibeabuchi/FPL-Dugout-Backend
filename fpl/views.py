import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.http import JsonResponse



BASE_URL = "https://fantasy.premierleague.com/api"

class FetchFPLGeneralInfoView(APIView):
    """Fetch general FPL information including gameweeks, teams, players, etc."""
    def get(self, request):
        url = f"{BASE_URL}/bootstrap-static/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FetchFPLTeamView(APIView):
    """Fetch an FPL manager's details using their team ID."""
    permission_classes = ''
    def get(self, request, teamId):
        url = f"{BASE_URL}/entry/{teamId}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        




class FetchFPLFixturesView(APIView):
    """Fetch all fixtures or upcoming fixtures."""
    def get(self, request):
        url = f"{BASE_URL}/fixtures/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PlayerDetailView(APIView):
    """Fetch detailed data for a specific player."""
    def get(self, request, player_id):
        url = f"{BASE_URL}/element-summary/{player_id}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class PlayerPhotoView(APIView):
    """Fetch photo for a specific player."""
    
    def get(self, request, opta_code):
        url = f"https://resources.premierleague.com/premierleague/photos/players/110x140/{opta_code}.png"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            return Response({"url": url}, status=status.HTTP_200_OK)  # ✅ Return the image URL

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class LiveGameweekDataView(APIView):
    """Fetch live data for a specific gameweek."""
    def get(self, request, event_id):
        url = f"{BASE_URL}/event/{event_id}/live/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FetchFPLTeamHistoryView(APIView):
    """Fetch an FPL manager's history, including past seasons and gameweek data."""
    def get(self, request, teamId):
        url = f"{BASE_URL}/entry/{teamId}/history/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FetchFPLTransfersView(APIView):
    """Fetch an FPL manager's transfer history."""
    def get(self, request, teamId):
        url = f"{BASE_URL}/entry/{teamId}/transfers/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FetchFPLLeagueView(APIView):
    """Fetch details of a classic FPL league."""
    def get(self, request, leagueId, page=1):
        url = f"{BASE_URL}/leagues-classic/{leagueId}/standings/?page_standings={page}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FetchFPLH2HLeagueView(APIView):
    """Fetch details of a head-to-head FPL league."""
    def get(self, request, leagueId):
        url = f"{BASE_URL}/leagues-h2h-matches/league/{leagueId}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FetchFullTeamDetailsView(APIView):
    """Fetch an FPL manager's team for a specific gameweek."""
    def get(self, request, teamId, gw):
        url = f"{BASE_URL}/entry/{teamId}/event/{gw}/picks/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EventStatusView(APIView):
    """Fetch the status of ongoing FPL events."""
    def get(self, request):
        url = f"{BASE_URL}/event-status/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class FetchFPLLeagueView(APIView):
#     permission_classes = ''
#     def get(self, request, league_id, page):
#         fpl_url = f"{BASE_URL}/leagues-classic/{league_id}/standings?page_standings={page}"
        
#         try:
#             response = requests.get(fpl_url)
#             response.raise_for_status()
#             data = response.json()
#             # print(data)
            
#             return Response(data, status=status.HTTP_200_OK)

#         except requests.exceptions.RequestException as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def get_league_players_and_teams(league_id, gameweek):
    """Fetch all players in a league and list managers who own each player."""
    
    # Get league standings
    league_url = f"{BASE_URL}/leagues-classic/{league_id}/standings/"
    league_data = requests.get(league_url).json()
    
    # Get FPL player database
    players_url = f"{BASE_URL}/bootstrap-static/"
    players_data = requests.get(players_url).json()
    player_dict = {p["id"]: p["web_name"] for p in players_data["elements"]}

    player_ownership = {}  # {player_name: [manager1, manager2, ...]}

    for manager in league_data['standings']['results']:
        team_id = manager['entry']
        team_url = f"{BASE_URL}/entry/{team_id}/event/{gameweek}/picks/"
        team_data = requests.get(team_url).json()

        for player in team_data["picks"]:
            player_id = player["element"]
            player_name = player_dict.get(player_id, "Unknown Player")

            if player_name not in player_ownership:
                player_ownership[player_name] = []

            player_ownership[player_name].append(manager["player_name"])

    return {"players": list(player_ownership.keys()), "ownership": player_ownership}

def get_players(request, league_id, gameweek):
    """API endpoint to return all players in the league and their owners."""
    data = get_league_players_and_teams(league_id, gameweek)
    return JsonResponse(data)