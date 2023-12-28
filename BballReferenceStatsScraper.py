import bs4, requests, lxml, re
from bs4 import BeautifulSoup
import pandas as pd


print("I learned how to web scrape, problem solve in code, and how to manage my working time during the duration of this project. Web scraping was a new thing for me. Though we did go over it a little in class, I first learned about it when we were originally talking about project ideas and what others have done in the past. I researched it, with the idea of getting data from ESPN, but I soon realized that that wasn't really a possibility because of restrictions ESPN has. The next place I checked was Basketball Reference, and thankfully they actually kind of encourage web scraping. I even found some source code that was based on pulling playoff data off of Basketball Reference, so I decided I’d try to modify it to get the stats that I wanted. It took me way too long, and often I would just get so tired and frustrated that I would end up watching some Python-related Ted Talk so I could continue to get hours, but didn’t have to smack my head against a wall. I continuously ran into the problem of it only scraping the first 30 rows and I honestly had no clue why. It didn’t seem to affect the source code, which still gave all the information the author wanted it to give. I eventually realized, after being stuck trying to analyze every part of rows_data, because it made sense that that was the limiting factor, and not finding anything wrong with it. I kept looking up how to manipulate how many rows of output and everything, but found nothing useful. Finally, I realized that it was in row 70, where the source code had team_stats work in the range of 0:len(row_titles), but for some reason the code stated earlier that row_titles = titles, which meant there were only 30 rows (as there were 30 titles) that were being scraped. It was smooth sailing from there and I put it in an excel sheet and brainstormed/researched a little about possible stats to make, then made my own, considering weighting and how much each stat is worth before I came up with the stats I did. I also did side project where I coded it for another page, but for some reason the reindexing wasn’t working correctly and I kept get an indexing error, but when I didn’t define the columns at the beginning of the code (I tried a lot of things before this), it weirdly worked. So, now I have an excel sheet for that, but I’m not sure what I’ll do with that yet. One of the biggest things I learned through my first semester of coding is that patience is key. Coming back to something with a clear mind can do wonders and just allowing a brain break can get the juices flowing again. Yeah, just that if you don’t succeed at first, do a little research, ask some questions, and you’ll be able to figure it out if you’re willing to work through a little frustration and not immediately give up.")


#Code partially sourced/adapted from Michael O'Donnell

final_df = pd.DataFrame(columns = ['Rk', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'])
#I changed the column names to be applicable to the page I was on

#rows = []
#for i in range(1,455):
    #rows.append(i)

#final_df = pd.DataFrame(rows)

#print(final_df.shape)

result = requests.get('https://www.basketball-reference.com/leagues/NBA_2023_totals.html')
#I changed the site

src = result.content

soup = BeautifulSoup(src, 'lxml')
#I used a different system to get the contents and use Beautiful Soup, specifically the one we learned in class

titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
#print(titles)

#getting row data
rows = soup.findAll('tr')[1:]
rows_data = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]

#print(len(rows))

#only column headers
headers = titles[1:titles.index("Rk")+1]

#print(titles.index('Rk'))
#print(titles.index('Rk')+1)
#print(headers)

#exclude duplicates of column headers
#titles = titles[titles.index("Rk")+1:]
#I excluded this part of the code, as duplicates didn't apply for me and I wanted to condense the code

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
#This part was a big trip up, I think it was the main limiter in getting all of the data, it was len(row_titles) before

#print(team_stats)

#add team name to each row in team_stats
for i in range(0, len(team_stats)):
    team_stats[i].insert(0, rows[i])

# add team, year columns to headers
#headers.insert(0, "Team")

year_standings = pd.DataFrame(team_stats, columns = titles)
#I changed it to columns = titles instead of columns = headers

# append new dataframe to final_df
final_df = final_df.append(year_standings)

print(final_df.info)

# export to csv
final_df.to_csv("nba_team_data.csv", index=False)

