Must-Haves
 Roster
-   Current best known method:
-     When going from captain select screen to css, set the following structs
-     803C676E - indicators for which roster spots have been filled - set to all 1s
-     803C6726 - character IDs - set based on HUD file
-     803C674A - chem with captain. Optional since we will overwrite set the stars in game
-     80750C7F - OK button available to press indicators. Set to 1 for each team. Then press up from "random" to "ok", and select ok. The game will move on to the lineup screen with the right roster.
  Star players
-   This function is the one that runs when a player is starred 800426dc
-   Also relevant is this address which indicates if the game is in the process of making a character a superstar. 8033677e (2 bytes, one for each team). It runs the above function and more.
  Batting order starting at who's currently up to bat
-   The batting order is initially set (including copying the character stats to InMemRoster) based on the CharID order in this array: 803C6726
-   Then, 80065dec sets the initial order based on an algorithm that considers character class, and overwrites InMemRoster with the stats of the new batting order.
-   Our best solution is to nop calls to 80065dec (nops occuring at 80047dec and 80047df4  seem like what we want) so the batting order can just be how we set up the charID array.
  Defensive alignment
-   803C6738 is the struct for the position of each character on the CSS
   Handedness
-   Found in inMemRoster struct 80353be0
  Team stars
-   In-game addresses: 80892ad6, 80892ad7 (bytes)
-   Probably easiest to deal with in-game while changing scores/innings/etc
 Inning
-   Inning number: 808928A0 (int), half inning: 8089294D (byte)
-   Seems like it can be simply changed anytime after the game starts
 Balls/strikes/outs
-   Strikes: 80892968, Balls: 8089296C, Outs: 80892970 (ints)
-   Stored outs (80892974) might also need to be edited to ensure no weird behavior.
-   Seems like these can be simply changed anytime after the game starts
 Scores
-   Away: 808928A4, Home: 808928CA (shorts)
-   Seems like it can be simply changed anytime after the game starts

Nice-to-Haves
- Prior inning scores
- Stats updated
