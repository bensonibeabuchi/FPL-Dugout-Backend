import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.http import JsonResponse
import asyncio
import httpx
from asgiref.sync import async_to_sync



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
    """Fetch details of a classic FPL league from pages 1 to 4 and merge results."""
    
    def get(self, request, leagueId):
        combined_results = []
        
        for page in range(1, 5):  # Fetch pages 1 to 5
            url = f"{BASE_URL}/leagues-classic/{leagueId}/standings/?page_standings={page}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                if "standings" in data and "results" in data["standings"]:
                    combined_results.extend(data["standings"]["results"])
                
                # Capture the first response structure for metadata (league details)
                if page == 1:
                    full_league_data = data
            
            except requests.exceptions.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Merge results into the first response data
        if full_league_data:
            full_league_data["standings"]["results"] = combined_results
            return Response(full_league_data, status=status.HTTP_200_OK)
        
        return Response({"error": "Failed to fetch league data"}, status=status.HTTP_400_BAD_REQUEST)

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


def get_league_players_and_teams(leagueId, gw):
    """Fetch all players in a league and list managers who own each player."""
    
    # Get league standings
    league_url = f"{BASE_URL}/leagues-classic/{leagueId}/standings/"
    league_data = requests.get(league_url).json()
    
    # Get FPL player database
    players_url = f"{BASE_URL}/bootstrap-static/"
    players_data = requests.get(players_url).json()
    player_dict = {p["id"]: p["web_name"] for p in players_data["elements"]}

    player_ownership = {}  # {player_name: [manager1, manager2, ...]}

    for manager in league_data['standings']['results']:
        team_id = manager['entry']
        team_url = f"{BASE_URL}/entry/{team_id}/event/{gw}/picks/"
        team_data = requests.get(team_url).json()

        for player in team_data["picks"]:
            player_id = player["element"]
            player_name = player_dict.get(player_id, "Unknown Player")

            if player_name not in player_ownership:
                player_ownership[player_name] = []

            player_ownership[player_name].append(manager["player_name"])

    return {"players": list(player_ownership.keys()), "ownership": player_ownership}

def get_players(request, leagueId, gw):
    """API endpoint to return all players in the league and their owners."""
    data = get_league_players_and_teams(leagueId, gw)
    return JsonResponse(data)

class FetchTeamEventPointsView(APIView):
    """Fetch and calculate an FPL manager's total event points for a specific gameweek."""

    def get(self, request, teamId, gw):
        # Fetch full team details
        team_url = f"{BASE_URL}/entry/{teamId}/event/{gw}/picks/"
        live_url = f"{BASE_URL}/event/{gw}/live/"

        try:
            team_response = requests.get(team_url)
            team_response.raise_for_status()
            team_data = team_response.json()

            live_response = requests.get(live_url)
            live_response.raise_for_status()
            live_data = live_response.json()

            # Extract player picks and live gameweek elements
            picks = team_data.get("picks", [])
            elements = {player["id"]: player["stats"]["total_points"] for player in live_data.get("elements", [])}

            # Calculate total team points
            total_team_points = sum(
                (elements.get(player["element"], 0) * player.get("multiplier", 1))
                for player in picks
            )

            # Calculate eventRealPoints
            event_transfers_cost = team_data.get("entry_history", {}).get("event_transfers_cost", 0)
            event_real_points = total_team_points - event_transfers_cost

            return Response({
                "teamId": teamId,
                "gameweek": gw,
                "total_team_points": total_team_points,
                "event_real_points": event_real_points,
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FetchTeamLiveTotalPointsView(APIView):
    """Fetch an FPL manager's live total points, combining past history with current gameweek points."""

    def get(self, request, teamId, gw):
        history_url = f"{BASE_URL}/entry/{teamId}/history/"
        event_points_url = f"{BASE_URL}/entry/{teamId}/event/{gw}/picks/"
        live_url = f"{BASE_URL}/event/{gw}/live/"

        try:
            # Fetch team history
            history_response = requests.get(history_url)
            history_response.raise_for_status()
            history_data = history_response.json()

            # Get total points from last completed gameweek
            past_gws = history_data.get("current", [])

            # Check the length of the history data
            length = len(past_gws)

            # If the length is 1, use the first event's total points, else use the total points from the last event
            if length == 1:
                last_recorded_total_points = past_gws[0]["total_points"]
            else:
                last_completed_gw = past_gws[length - 2]["event"]
                last_recorded_total_points = past_gws[length - 2]["total_points"]

            # print(last_recorded_total_points)

            # Fetch full team details for the current GW
            team_response = requests.get(event_points_url)
            team_response.raise_for_status()
            team_data = team_response.json()

            live_response = requests.get(live_url)
            live_response.raise_for_status()
            live_data = live_response.json()

            # Extract player picks and live gameweek elements
            picks = team_data.get("picks", [])
            elements = {player["id"]: player["stats"]["total_points"] for player in live_data.get("elements", [])}

            # Calculate total team points for current GW
            total_team_points = sum(
                (elements.get(player["element"], 0) * player.get("multiplier", 1))
                for player in picks
            )

            # Deduct event transfer cost
            event_transfers_cost = team_data.get("entry_history", {}).get("event_transfers_cost", 0)
            event_real_points = total_team_points - event_transfers_cost

            # Calculate Live Total Points
            live_total_points = last_recorded_total_points + event_real_points

            return Response({
                "teamId": teamId,
                "gameweek": gw,
                "last_recorded_total_points": last_recorded_total_points,
                "event_real_points": event_real_points,
                "live_total_points": live_total_points,
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class FetchLeagueLiveTotalPointsView(APIView):
#     """Fetch live total points for all teams in a league."""

#     def get(self, request, leagueId):
#         gw = request.GET.get("gw")  # 🔹 Get gw from query parameters

#         if not gw:
#             return Response({"error": "Gameweek (gw) parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             gw = int(gw)  # Ensure gw is an integer
#         except ValueError:
#             return Response({"error": "Invalid gw parameter. Must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        
#         combined_results = []
#         for page in range(1, 5):  # Fetch pages 1 to 4
#             league_url = f"{BASE_URL}/leagues-classic/{leagueId}/standings/?page_standings={page}"

#             try:
#                 # Fetch league standings
#                 league_response = requests.get(league_url)
#                 league_response.raise_for_status()
#                 league_data = league_response.json()

#                 if "standings" in league_data and "results" in league_data["standings"]:
#                     combined_results.extend(league_data["standings"]["results"])

#             except requests.exceptions.RequestException as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
#             live_points_list = []
            
#             for team in combined_results:
#                 teamId = team.get("entry")
#                 if teamId:
#                     live_points = self.get_team_live_points(teamId, gw)
#                     live_points_list.append(live_points)

#             return Response(live_points_list, status=status.HTTP_200_OK)

#     def get_team_live_points(self, teamId, gw):
#         """Fetch live total points for a single team."""
#         history_url = f"{BASE_URL}/entry/{teamId}/history/"
#         event_points_url = f"{BASE_URL}/entry/{teamId}/event/{gw}/picks/"
#         live_url = f"{BASE_URL}/event/{gw}/live/"

#         try:
#             # Fetch team history
#             history_response = requests.get(history_url)
#             history_response.raise_for_status()
#             history_data = history_response.json()

#             # Get total points from last completed gameweek
#             past_gws = history_data.get("current", [])
#             length = len(past_gws)
#             if length == 1:
#                 last_recorded_total_points = past_gws[0]["total_points"]
#             else:
#                 last_completed_gw = past_gws[length - 2]["event"]
#                 last_recorded_total_points = past_gws[length - 2]["total_points"]

#             # Fetch full team details for the current GW
#             team_response = requests.get(event_points_url)
#             team_response.raise_for_status()
#             team_data = team_response.json()

#             live_response = requests.get(live_url)
#             live_response.raise_for_status()
#             live_data = live_response.json()

#             # Extract player picks and live gameweek elements
#             picks = team_data.get("picks", [])
#             elements = {player["id"]: player["stats"]["total_points"] for player in live_data.get("elements", [])}

#             # Calculate total team points for current GW
#             total_team_points = sum(
#                 (elements.get(player["element"], 0) * player.get("multiplier", 1))
#                 for player in picks
#             )

#             # Deduct event transfer cost
#             event_transfers_cost = team_data.get("entry_history", {}).get("event_transfers_cost", 0)
#             event_real_points = total_team_points - event_transfers_cost

#             # Calculate Live Total Points
#             live_total_points = last_recorded_total_points + event_real_points

#             return {
#                 "teamId": teamId,
#                 "gameweek": gw,
#                 "last_recorded_total_points": last_recorded_total_points,
#                 "event_real_points": event_real_points,
#                 "live_total_points": live_total_points,
#             }

#         except requests.exceptions.RequestException:
#             return {
#                 "teamId": teamId,
#                 "gameweek": gw,
#                 "last_recorded_total_points": 0,
#                 "event_real_points": 0,
#                 "live_total_points": 0,
#             }


class FetchLeagueLiveTotalPointsView(APIView):
    """Fetch live total points for all teams in a league asynchronously."""

    async def fetch_league_page(self, client, leagueId, page):
        """Fetches a single page of league standings asynchronously."""
        league_url = f"{BASE_URL}/leagues-classic/{leagueId}/standings/?page_standings={page}"
        try:
            response = await client.get(league_url)
            response.raise_for_status()
            league_data = response.json()
            return league_data.get("standings", {}).get("results", [])
        except Exception:
            return []

    async def fetch_all_league_teams(self, leagueId):
        """Fetches all teams from all pages asynchronously."""
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_league_page(client, leagueId, page) for page in range(1, 5)]
            results = await asyncio.gather(*tasks)

        # Flatten the list of lists into a single list
        return [team for page_results in results for team in page_results]

    async def fetch_team_live_points(self, client, teamId, gw):
        """Fetches live total points for a team asynchronously."""
        history_url = f"{BASE_URL}/entry/{teamId}/history/"
        event_points_url = f"{BASE_URL}/entry/{teamId}/event/{gw}/picks/"
        live_url = f"{BASE_URL}/event/{gw}/live/"

        try:
            responses = await asyncio.gather(
                client.get(history_url),
                client.get(event_points_url),
                client.get(live_url),
                return_exceptions=True
            )

            history_response, team_response, live_response = responses

            if isinstance(history_response, Exception) or isinstance(team_response, Exception) or isinstance(live_response, Exception):
                return {"teamId": teamId, "gameweek": gw, "live_total_points": 0}

            history_data = history_response.json()
            team_data = team_response.json()
            live_data = live_response.json()

            # Get total points from last completed gameweek
            past_gws = history_data.get("current", [])
            last_recorded_total_points = past_gws[-2]["total_points"] if len(past_gws) > 1 else past_gws[0]["total_points"]

            # Extract player picks and live gameweek elements
            picks = team_data.get("picks", [])
            elements = {player["id"]: player["stats"]["total_points"] for player in live_data.get("elements", [])}

            # Calculate total team points for current GW
            total_team_points = sum(
                (elements.get(player["element"], 0) * player.get("multiplier", 1))
                for player in picks
            )

            # Deduct event transfer cost
            event_transfers_cost = team_data.get("entry_history", {}).get("event_transfers_cost", 0)
            event_real_points = total_team_points - event_transfers_cost

            # Calculate Live Total Points
            live_total_points = last_recorded_total_points + event_real_points

            return {
                "teamId": teamId,
                "gameweek": gw,
                "last_recorded_total_points": last_recorded_total_points,
                "event_real_points": event_real_points,
                "live_total_points": live_total_points,
            }

        except Exception:
            return {"teamId": teamId, "gameweek": gw, "live_total_points": 0}

    def get(self, request, leagueId):
        """Sync wrapper for Django's APIView to call async function."""
        return async_to_sync(self.async_get)(request, leagueId)

    async def async_get(self, request, leagueId):
        gw = request.GET.get("gw")

        if not gw:
            return Response({"error": "Gameweek (gw) parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gw = int(gw)
        except ValueError:
            return Response({"error": "Invalid gw parameter. Must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        teams = await self.fetch_all_league_teams(leagueId)

        # Fetch all live points in parallel
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_team_live_points(client, team.get("entry"), gw) for team in teams if team.get("entry")]
            live_points_list = await asyncio.gather(*tasks)

        # Calculate the highest live total points in the league
        highest_live_points = max((team["live_total_points"] for team in live_points_list), default=0)

        return Response({
            "highest_live_points": highest_live_points,
            "teams_live_points": live_points_list
        }, status=status.HTTP_200_OK)