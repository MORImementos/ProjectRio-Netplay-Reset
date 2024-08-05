import json
from resources import reverse_mappings, captain_ids, character_type

hud = json.load(open('decoded.hud.json'))

#get character ID list
original_rosters = []
homeCharIDs = []
i = 0
team = "Away"
while i < 2:
      team_ids = []
      j = 0
      while j < 9:
            team_ids.append(reverse_mappings[hud["%s Roster %s" % (team, j)]["CharID"]])
            j += 1
      original_rosters.append(team_ids)
      team = "Home"
      i += 1

print(original_rosters)

teamBatting = hud["Half Inning"]
teamFielding = 1 - teamBatting

#determine batting order for team currently up to bat
batterUpToBat = hud["Batter Roster Loc"]
i = 0
team_batting_battingOrder = []
while i < 9:
      team_batting_battingOrder.append(original_rosters[teamBatting][(batterUpToBat + i) % 9])
      i += 1

#determine batting order for team currently fielding
team = "Home" if (teamFielding == 1) else "Away"
i = 0
max_pa = 0
max_pa_rosterLoc = 0
while i < 9:
      oStats = hud["%s Roster %s" % (team, i)]["Offensive Stats"]
      
      current_pa = oStats["At Bats"] + oStats["Walks (4 Balls)"] + oStats["Walks (Hit)"]
      
      if current_pa >= max_pa:
            max_pa = current_pa
            max_pa_rosterLoc = i
      
      i += 1

i = 0
team_fielding_battingOrder = []
while i < 9:
      # + 1 since we want batter after one with most PAs
      team_fielding_battingOrder.append(original_rosters[teamFielding][(max_pa_rosterLoc + 1 + i) % 9])
      i += 1
      
def adjustRoster(charIDs):
      #adjusts roster order to allow batting order to not be random if possible.
      #if more than 6 of one character type, then we will move all of them to the end of 
      #the roster list to avoid randomness when the batting order is set.

      charType_counts = [0, 0, 0, 0]
      for char in charIDs:
            charType_counts[character_type[char]] += 1

      if max(charType_counts) < 6:
            #no adjustment needed
            return charIDs

      mostFreqType = max(range(4), key=charType_counts.__getitem__)
      print(mostFreqType)

      # swap all characters of the most frequent type to the end of the roster
      i = 0
      while i < max(charType_counts):
            if character_type[charIDs[i]] == mostFreqType:
                  j = 8
                  while j > i:
                        if character_type[charIDs[j]] != mostFreqType:
                              #swap characters
                              oldCharID = charIDs[j]
                              charIDs[j] = charIDs[i]
                              charIDs[i] = oldCharID
                              break
                        else:
                              j -= 1
            i += 1
      
      return charIDs
      
adjusted_rosters = []
adjusted_rosters.append(adjustRoster(original_rosters[0]))
adjusted_rosters.append(adjustRoster(original_rosters[1]))
      
#put final gecko code together
geckoCode = ""

#make part of gecko code that sets the character selected indicators on character select screen
geckoCode = geckoCode + "003C676E 00110001"

#make OK buttons active on character select screen
geckoCode = geckoCode + "\n00750C7F 00010001"

#put cursors on OK buttons
geckoCode = geckoCode + "\n04750c48 00000009\n04750c4C 00000009"

#make part of gecko code that puts character IDs into the roster
aRosterIDs = 0x803C6726

i = 0
while i < 2:
      j = 0
      while j < 9:
            geckoCode = geckoCode + "\n00" + hex(aRosterIDs + i * 9 + j)[4:]
            nZeros = 7 if adjusted_rosters[i][j] < 16 else 6
            geckoCode = geckoCode + " " + nZeros * "0" + hex(adjusted_rosters[i][j])[2:]
            j += 1
      i += 1

#batting order part of code
#until a better solution is found, our best solution is to adjust the batting order priority struct
i = 0
batting_order_types = [[0], [0]]
while i < 2:
      #find type of latest captain character
      j = 8
      last_captain_index = 8
      while j > 0:
            if adjusted_rosters[i][j] in captain_ids:
                  batting_order_types[i][0] = character_type[adjusted_rosters[i][j]]
                  last_captain_index = j
                  break
            j -= 1
      
      #set rest of the types order
      j = 0
      while j < 9:
            if j == last_captain_index:
                  j += 1
                  continue #skip the captain one since they're first in the list
            batting_order_types[i].append(character_type[adjusted_rosters[i][j]])
            j += 1

      print(batting_order_types)
      i += 1

aBattingOrderPriority = 0x80109054
nPioritySpotsUsed = [0, 0, 0, 0]

i = 0
while i < 2:
      j = 0
      while j < 9:
            current_type = character_type[batting_order_types[i][j]]
            geckoCode += "\n00" + hex(aBattingOrderPriority + i * 9 + j)[4:] + " " + "0" * 7 + str(current_type)
            j += 1
      i += 1


# IN GAME VALUES

# set if statement to see if the starting indicator is not set yet.
#its a 16 but write since I can't find the code for an 8 bit write, but the address before it is 0 at the start of the game
geckoCode += "\n28892ab4 00000000" #start if statement

#inning
geckoCode += "\n048928A0 0000000" + hex(hud["Inning"])[2:]
geckoCode += "\n0089294D 0000000" + str(hud["Half Inning"])

#scores
homeScore = hud["Home Score"]
awayScore = hud["Away Score"]

homeScoreZeros = 7 if homeScore < 16 else 6
awayScoreZeros = 7 if awayScore < 16 else 6

geckoCode += "\n028928A4 " + awayScoreZeros * "0" + hex(awayScore)[2:]
geckoCode += "\n028928CA " + homeScoreZeros * "0" + hex(homeScore)[2:]

#count
geckoCode += "\n04892968 0000000" + str(hud["Strikes"])
geckoCode += "\n0489296C 0000000" + str(hud["Balls"])
geckoCode += "\n04892970 0000000" + str(hud["Outs"])
geckoCode += "\n04892974 0000000" + str(hud["Outs"]) #stored outs

#runners
aNopLocation = 0x806c93f0
nopLocGap = 0x30 
aRosterID0 = 0x8088eef8
rosterIDGap = 0x154
runnerJsonKeys = ["Runner Batter", "Runner 1B", "Runner 2B", "Runner 3B"]

for runnerKey in runnerJsonKeys:
      if runnerKey in hud:
            resultBase = hud[runnerKey]["Runner Result Base"]
            if resultBase in [1, 2, 3]:
                  runnerCharID = reverse_mappings[hud[runnerKey]["Runner Char Id"]]
                  runnerRosterSpot = team_batting_battingOrder.index(runnerCharID)
                  zerosCharID = 7 if runnerCharID < 16 else 6

                  geckoCode += "\n02" + hex(aRosterID0 + rosterIDGap * resultBase)[4:] + " 0000000" + str(runnerRosterSpot)
                  geckoCode += "\n02" + hex(aRosterID0 + rosterIDGap * resultBase + 2)[4:] + " " + zerosCharID * "0" + hex(runnerCharID)[2:]
                  geckoCode += "\n04" + hex(aNopLocation + nopLocGap * resultBase)[4:] + " 60000000"


      

print(geckoCode)