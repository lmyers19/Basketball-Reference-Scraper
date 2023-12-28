import bs4, requests, lxml, re
from bs4 import BeautifulSoup
import pandas as pd


#Code partially sourced/adapted from Michael O'Donnell

final_df = pd.DataFrame(columns = ['Rk', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])

#rows = []
#for i in range(1,455):
    #rows.append(i)

#final_df = pd.DataFrame(rows)

#print(final_df.shape)

result = requests.get('https://www.basketball-reference.com/leagues/NBA_2023_totals.html')
#change the ip address to what you need

src = result.content

soup = BeautifulSoup(src, 'lxml')
#I used a different system to get the contents and use Beautiful Soup, specifically the one we learned in class

titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
#print(titles)

#getting row data
rows = soup.findAll('tr')[1:]
rows_data = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]


#only column headers
headers = titles[1:titles.index("Rk")+1]


try:
    row_titles = titles[:titles.index('454')]
    #I changed this part to the number of rows, instead of the heading they used before

except: row_titles = titles

for i in headers:
    row_titles.remove(i)

#print(len(row_titles))
#print(len(rows))

team_stats = [[td.getText() for td in rows[i].findAll('td')]
        for i in range(len(rows))]
# remove empty elements
team_stats = [e for e in team_stats if e != []]
# only keep needed rows
team_stats = team_stats[0:len(rows)]

#print(team_stats)

#add team name to each row in team_stats
for i in range(0, len(team_stats)):
    team_stats[i].insert(0, rows[i])

# add team, year columns to headers
#headers.insert(0, "Team")

year_standings = pd.DataFrame(team_stats, columns = titles)

# append new dataframe to final_df
final_df = final_df.append(year_standings)

print(final_df.info)

# export to csv
final_df.to_csv("nba_team_data.csv", index=False)

