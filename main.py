#########################
### Creating a simple program to scrape info from basketball-reference.com
### Function takes in a URL that is a PLAYER base stats page
### Outputs a list of all players they have ever assisted, and the number of assists to that player
### November 8, 2021
### Cade Cunningham will be the greatest basketball player of all time
#########################


#############################
#### Scroll down to "your code here"
#### to see where to edit to get tables for other players
#############################

import requests
from bs4 import BeautifulSoup
from pprint import pprint

def getID(siteurl):
    #site is sitename/players/initial/uniqueID.html
    #want to grab uniqueID from that
    newstring = siteurl[47:]
    newstring = newstring[0:newstring.find(".html")]
    return newstring

def getPlayerName(soupy):
    titleline = str(soupy.find("title"))
    nstart = titleline.find(">")
    nend = titleline.find(" Stats")
    return titleline[nstart+1:nend]

def findScorer(linestring):
    nstart = linestring.find("/players/")
    nend = linestring.find(".html")
    return linestring[nstart+11:nend]



def getAssists(siteurl):
    # site is sitename/players/initial/uniqueID.html
    # want to grab uniqueID from that
    myID = getID(siteurl)

    ##grab site data
    basesiteinfo = requests.get(siteurl)

    ##parse HTML and save to BS object
    basesoup = BeautifulSoup(basesiteinfo.text, "html.parser")

    # get player info
    # player name
    # list of years player played
    playerName = getPlayerName(basesoup)
    years = []

    # This will be the base data output
    # a list of all assists ever made
    # will need to clean it up after
    assistlog = []

    for link in basesoup.find_all('a'):
        str1 = str(link.get('href'))
        if str1.find('gamelog') > -1:
            if str1 not in years:
                if str1.find("playoff") == -1:
                    years.append(str1)

    # go through each year and process each game log
    allgames = []
    for y in years:
        yearsoupurl = "https://www.basketball-reference.com" + y
        yearsoupinfo = requests.get(yearsoupurl)
        yearsoup = BeautifulSoup(yearsoupinfo.text, "html.parser")

        # find list of game logs in year page
        for link in yearsoup.find_all('a'):
            str1 = str(link.get('href'))
            if str1.find('/boxscores/') > -1:
                if str1 not in allgames:
                    if str1.find(".html") > -1:
                        str1 = str1[str1.find("s/") + 1:]
                        allgames.append(str1)

    #not sure why there's still repeats but setting uniques in list of games
    #makes the list of games go out of order, but oh well
    uniquegames = set(allgames)
    # go through each game in list and process it
    strsearch = '(assist by <a href="/players/' + myID[0] + '/' + myID + '.html">'
    for game in uniquegames:
        gameurl = "https://www.basketball-reference.com/boxscores/pbp" + game
        print(gameurl)
        gamesoupinfo = requests.get(gameurl)
        gamesoup = BeautifulSoup(gamesoupinfo.text, "html.parser")
        for line in gamesoup.find_all('td'):
            str1 = str(line)
            if str1.find(strsearch) > -1:
                scorer = findScorer(str1)
                assistlog.append(scorer)

    outdata = []
    scorers = set(assistlog)
    for player in scorers:
        assists = assistlog.count(player)

        #use getPlayerName process to get actual name from ID of scoring player
        tempurl = "https://www.basketball-reference.com/players/" + player[0] + "/" + player + ".html"
        tempurlsoupinfo = requests.get(tempurl)
        tempsoup = BeautifulSoup(tempurlsoupinfo.text, "html.parser")
        playername = getPlayerName(tempsoup)

        item = (playername, assists)
        outdata.append(item)

    outdata = sorted(outdata, key=lambda tup:tup[1], reverse=True)
    pprint(outdata)


#############################
#### your code here
#### below are commented out (# at begining of line means comment) example calls
#### copy the line with the URL of the player you want assist info on
#### and dont comment out the line
#### then hit the green arrow to run it
#### right now the program prints out each game url as it goes so you know its working
#### can take quite a bit for players with a lot of games
#### try a rookie first to make sure everything is working
#### highly recommend running only one at a time

#### NOTE MAKE SUER TO GET THE WHOLE URL STARTING WITH https:
#### I CODED THIS THING IN AN HOUR ITS JANKY AF
#############################

## Lebron James
#getAssists("https://www.basketball-reference.com/players/j/jamesle01.html")

## Jordan Poole
#getAssists("https://www.basketball-reference.com/players/p/poolejo01.html")

## Jerami Grant
#getAssists("https://www.basketball-reference.com/players/g/grantje01.html")

## Steph Curry
#getAssists("https://www.basketball-reference.com/players/c/curryst01.html")

##if you want to get your output in reddit table format
## copy the following into a new project and run
## input = <paste your output here, including the brackets []>
##counter = 1
##for line in input:
##    print("| " + str(counter) + " | " + line[0] + " | " + str(line[1]))
##    counter = counter + 1
