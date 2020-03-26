"""# Json"""

#json基本使用方式
import requests
request_url = "http://data.nba.net/prod/v2/2019/teams.json"
response = requests.get(request_url)
teams = response.json()
print(type(teams))
print(teams)

print(type(response))
print(response.status_code)

#觀察json方法
response_json = response.json()
print(type(response_json))
print(response_json)
print(response_json.keys())

#計算有幾隻NBA球隊
teams = response_json['league']['standard']
NBAteams = [team for team in teams if team['isNBAFranchise']]
num = len(NBAteams)
print(teams)
print(NBAteams)
print("2019-2020 球季 NBA 有 %i 支球隊"%num)

#有哪些球隊屬於Atlantic,有哪些球隊屬於SouthWest
Southwest_teams = [team['fullName'] for team in teams if team['divName']=='Southwest']
print(Southwest_teams)
Atlantic_team = [team['fullName'] for team in teams if team['divName']=='Atlantic']
print(Atlantic_team)

#把各分組對應的隊伍設為字典
team_dict = {}
for t in teams:
    div = t["divName"]
    full_name = t["fullName"]
    if div in team_dict:
        team_dict[div].append(full_name)
    else:
        team_dict[div] = [full_name]
print(team_dict)

#字典對應value為list時，創建及增添list內容的方式
teams_dict = {}
teams_dict['a']=['t1']
teams_dict['a'].append('t2')
print(teams_dict)
