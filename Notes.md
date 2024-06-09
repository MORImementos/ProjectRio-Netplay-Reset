Must-Haves
- Roster
- Star players
-   This function is the one that runs when a player is starred 800426dc
-   Also relevant is this address which indicates if the game is in the process of making a character a superstar. 8033677e (2 bytes, one for each team). It runs the above function and more.
- Defensive alignment
- Batting order starting at who's currently up to bat
- Handedness
-   Found in inMemRoster struct 80353be0
- Team stars
-   80892ad6, 80892ad7 (bytes)
-   Probably easiest to deal with in-game while changing scores/innings/etc
- Inning
-   Inning number: 808928A0 (int), half inning: 8089294D (byte)
-   Seems like it can be simply changed anytime after the game starts
- Balls/strikes/outs
-   Strikes: 80892968, Balls: 8089296C, Outs: 80892970 (ints)
-   Stored outs (80892974) might also need to be edited to ensure no weird behavior.
-   Seems like these can be simply changed anytime after the game starts
- Scores
-   Away: 808928A4, Home: 808928CA (shorts)
-   Seems like it can be simply changed anytime after the game starts

Nice-to-Haves
- Prior inning scores
- Stats updated
