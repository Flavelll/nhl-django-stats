# # nhl_app/views.py

from nhl_app.queries import build_filters

import json
from django.shortcuts import render
from .forms import TeamCompareForm
from .queries import (
    get_team_total,
    get_team_games,
    get_players_total,
    get_goalies_total,
    get_agg,
    get_compare_teams
)


def nhl_stats_view(request):
    form = TeamCompareForm(request.GET or None)

    team = ['FLA']
    seasons = [20242025]
    game_types = [2,3]
    team_total = None


    if form.is_valid():
        team = form.cleaned_data.get("team")
        seasons = [int(s) for s in form.cleaned_data['season']]
        game_types = [int(g) for g in form.cleaned_data['game_type']]

    context = {
        "form": form,
        "team": team,

        "team_total": get_team_total(team, seasons, game_types),
        "team_players": get_players_total(team, seasons, game_types),
        "team_games": get_team_games(team, seasons, game_types),
        "player_goalies": get_goalies_total(team, seasons, game_types),


    }
    return render(request, "nhl_app/index.html", context)


def nhl_agg_view(request):
    form = TeamCompareForm(request.GET or None)
    result = None
    compare = None
    teams = []
    opponents = []
    seasons = []
    gametypes = []

    if form.is_valid():

        seasons = [int(s) for s in form.cleaned_data.get("season") or []]
        gametypes = [int(g) for g in form.cleaned_data.get("game_type") or []]
        teams = form.cleaned_data.get("team") or []
        opponents = form.cleaned_data.get("opponent") or []

        compare = get_compare_teams(
            teams=teams,
            opponents=opponents,
            seasons=seasons,
            gametypes=gametypes,
    )



    context = {
        "form": form,
        "teams": teams,
        "team_agg": get_agg,
        "team_compare": compare,
    }

    return render(request, "nhl_app/agg.html", context)


