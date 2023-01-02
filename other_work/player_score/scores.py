import request, pandas
# working on scoring

def get_game_score(self, id):
    response = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(id))
    data = response.json()
    away = data['liveData']['boxscore']['teams']['away']['players']
    home = data['liveData']['boxscore']['teams']['home']['players']
    players = {**away, **home} 
    df = pandas.DataFrame(columns=['Name', 'Goals', 'Assists', 'Shots', 'Hits', 'Blocks', 'TOI', 'PenalyMinutes', 'GoalDifferential', 'GameScore'])
    for i in players:
        player = players.get(i)
        name = player['person']['fullName']
        position = player['position']['code']
        stats = player['stats']
        if position != "G" and len(stats) > 0:
            goals = player['stats']['skaterStats']['goals']
            assists = player['stats']['skaterStats']['assists']
            shots = player['stats']['skaterStats']['shots']
            hits = player['stats']['skaterStats']['hits']
            blocks = player['stats']['skaterStats']['blocked']
            giveaways = player['stats']['skaterStats']['giveaways']
            takeaways = player['stats']['skaterStats']['takeaways']
            pen = giveaways = player['stats']['skaterStats']['penaltyMinutes']
            plus_minus = giveaways = player['stats']['skaterStats']['plusMinus']
            TOI = player['stats']['skaterStats']['timeOnIce']
            TOI = TOI.replace(":", ".")
            TOI = float(TOI)
            game_score = (.75 * goals) + (.6 * assists) + (.075 * shots) + (.05 * blocks) + (.01 * hits) + (-.05 * giveaways) + (.02 * TOI) + (.05 * takeaways) + (-.07 * pen) + (.3 * plus_minus) 
            df.loc[len(df)] = [name, goals, assists, shots, hits, blocks, TOI, pen, plus_minus, game_score]
    #df = df.sort_values(by=['GameScore'], ascending=False)
    json = df.to_json()
    return df