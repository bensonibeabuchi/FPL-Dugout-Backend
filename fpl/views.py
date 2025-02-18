import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse


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
    def get(self, request, team_id):
        url = f"{BASE_URL}/entry/{team_id}/"
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
    def get(self, request, team_id):
        url = f"{BASE_URL}/entry/{team_id}/history/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FetchFPLTransfersView(APIView):
    """Fetch an FPL manager's transfer history."""
    def get(self, request, team_id):
        url = f"{BASE_URL}/entry/{team_id}/transfers/"
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
    def get(self, request, team_id, gw):
        url = f"{BASE_URL}/entry/{team_id}/event/{gw}/picks/"
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