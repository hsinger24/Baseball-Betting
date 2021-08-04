import requests
import json

# List of dictionaries with team_id and team_name as they appear in MLB API
teams = [
    {
        'team_id': '108',
        'team_name': 'Angels'
    }, {
        'team_id': '109',
        'team_name': 'Diamondbacks'
    }, {
        'team_id': '110',
        'team_name': 'Orioles'
    }, {
        'team_id': '111',
        'team_name': 'Red Sox'
    }, {
        'team_id': '112',
        'team_name': 'Cubs'
    }, {
        'team_id': '113',
        'team_name': 'Reds'
    }, {
        'team_id': '114',
        'team_name': 'Indians'
    }, {
        'team_id': '115',
        'team_name': 'Rockies'
    }, {
        'team_id': '116',
        'team_name': 'Tigers'
    }, {
        'team_id': '117',
        'team_name': 'Astros'
    }, {
        'team_id': '118',
        'team_name': 'Royals'
    }, {
        'team_id': '119',
        'team_name': 'Dodgers'
    }, {
        'team_id': '120',
        'team_name': 'Nationals'
    }, {
        'team_id': '121',
        'team_name': 'Mets'
    }, {
        'team_id': '133',
        'team_name': 'Athletics'
    }, {
        'team_id': '134',
        'team_name': 'Pirates'
    }, {
        'team_id': '135',
        'team_name': 'Padres'
    }, {
        'team_id': '136',
        'team_name': 'Mariners'
    }, {
        'team_id': '137',
        'team_name': 'Giants'
    }, {
        'team_id': '138',
        'team_name': 'Cardinals'
    }, {
        'team_id': '139',
        'team_name': 'Rays'
    }, {
        'team_id': '140',
        'team_name': 'Rangers'
    }, {
        'team_id': '141',
        'team_name': 'Blue Jays'
    }, {
        'team_id': '142',
        'team_name': 'Twins'
    }, {
        'team_id': '143',
        'team_name': 'Phillies'
    }, {
        'team_id': '144',
        'team_name': 'Braves'
    }, {
        'team_id': '145',
        'team_name': 'White Sox'
    }, {
        'team_id': '146',
        'team_name': 'Marlins'
    }, {
        'team_id': '147',
        'team_name': 'Yankees'
    }, {
        'team_id': '158',
        'team_name': 'Brewers'
    }
]


def _retrieve_team_active_roster(team_id):
    '''
    Gets the ~25 man active roster for a specific MLB team. Should not be used outside this file
    Params:
        - team_id {Integer}: the id of the team in the list above
    Returns:
        - An array of player names retrieved from the API
    '''
    url = f"http://lookup-service-prod.mlb.com/json/named.roster_40.bam?team_id=%27{team_id}%27"
    r = requests.get(url=url)
    data = r.json()

    players_all = data['roster_40']['queryResults']['row']

    players_active = []
    for player in players_all:
        if (player['status_code'] == 'A'):
            players_active.append((player['name_display_first_last'], player['player_id']))
    return players_active


def retrieve_all_active_rosters(file_name="data/active_rosters.json"):
    '''
    Downloads the active rosters for every MLB team and saves to given file_name (rosters.json)
    Params:
        - file_name=data/rosters.json
    Returns: 
        - A array of dictionaries where each element holds the team name and roster
    '''
    active_rosters = []
    for team in teams:
        active_rosters.append({
            'team_name': team['team_name'],
            'team_roster': _retrieve_team_active_roster(team['team_id'])
        })

    if file_name is not None:
        with open(file_name, "w") as f:
            f.write(json.dumps(active_rosters, indent=2))

    return active_rosters


def load_active_rosters(file_name= "data/active_rosters.json"):
    """Loads the active rosters from a saved file

    Args:
        file_name (str, optional): The json file to read the rosters. Defaults to "data/rosters.json".

    Returns:
        (list of dicts): a list of dicts, one dict for each team + roster
    """

    with open(file_name, "r") as f:
        active_rosters = json.load(f)
        return active_rosters


