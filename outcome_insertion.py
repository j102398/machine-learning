import sqlite3
import os

#Locate the prediction file by specifying the gameweek
gameweek = 28
pathToFile = f"C:\\Users\\joe\\PycharmProjects\\predictions\\predictions_archive\\predictions_gw{gameweek}.db"

#
#Connect to the previous database
previous_db_connection = sqlite3.connect(pathToFile)
previous_db_cursor = previous_db_connection.cursor()


#We want to connect to the fixture database for the final score, which will be inserted
fixture_file_path = "C:\\Users\\joe\\PycharmProjects\\fixture_db\\fixtures.db"
fixture_connection = sqlite3.connect(fixture_file_path)
fixture_db_cursor = fixture_connection.cursor()





#We want to store the outcome in a folder
def create_folder():
    folder_path = "outcomes_archive"
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print("Outcome archive folder created successfully.")
        except:
            print("Error creating folder")
    else:
        print("Folder already exists")

create_folder()


#Create a new outcome database
outcome_db_connection = sqlite3.connect(f'C:\\Users\\joe\\PycharmProjects\\outcome_insertion\\outcomes_archive\\gw{gameweek}_outcome.db')
outcome_db_cursor = outcome_db_connection.cursor()





#We want to insert the  columns into the new database
def insert_columns():
    query = """
    CREATE TABLE IF NOT EXISTS outcome (
        home_points INTEGER,
        home_last_5_points INTEGER,
        home_goal_diff INTEGER,
        home_progressive_carries INTEGER,
        home_progressive_passes INTEGER,
        home_xg REAL,
        home_previous_xg REAL,
        home_previous_goals INTEGER,
        away_points INTEGER,
        away_last_5_points INTEGER,
        away_goal_diff INTEGER,
        away_progressive_carries INTEGER,
        away_progressive_passes INTEGER,
        away_xg REAL,
        away_previous_xg REAL,
        away_previous_goals INTEGER,
        home_goals_in_game INTEGER,
        away_goals_in_game INTEGER
    )
    """
    try:
        outcome_db_cursor.execute(query)
    except:
        print("Either table exists or error creating new table:")


def retrieve_outcome(fixture):
    fixture_db_cursor.execute('SELECT score FROM fixtures WHERE fixture = ? ', (fixture,))
    score = fixture_db_cursor.fetchone()
    return score


def insert_outcome():
    # Retrieve all rows from the statistics table
    previous_db_cursor.execute('SELECT * FROM statistics')
    rows = previous_db_cursor.fetchall()


    # Iterate over each row
    for row in rows:
        # Unpack row values into variables
        (match_id, gameweek, home_team, away_team, previous_score, previous_away_xg, home_points,
         home_last_5_points, home_goal_diff, home_progressive_carries, home_progressive_passes,
         home_xg, previous_home_xg, null_value, away_points, away_last_5_points, away_goal_diff,
         away_progressive_carries,
         away_progressive_passes, away_xg, home_goals, away_goals, previous_home_goals,
         previous_away_goals) = row

        #Lookup the fixture in the fixture db to determine outcome
        fixture = home_team + " vs " + away_team
        final_score = retrieve_outcome(fixture)

        #Convert the tuple to string
        final_score_str = ''.join(final_score)

        #Split the scores up into home and away goals
        previous_score_split = previous_score.split('–')
        final_score_split = final_score_str.split('–')

        #Assign variables
        previous_home_goals,previous_away_goals = previous_score_split
        home_goals_in_game,away_goals_in_game = final_score_split


        #Insert all the new data
        query = """
            INSERT INTO outcome (
                home_points,
                home_last_5_points,
                home_goal_diff,
                home_progressive_carries,
                home_progressive_passes,
                home_xg,
                home_previous_xg,
                away_points,
                away_last_5_points,
                away_goal_diff,
                away_progressive_carries,
                away_progressive_passes,
                away_xg,
                away_previous_xg,
                home_goals_in_game,
                away_goals_in_game
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """


        outcome_db_cursor.execute(query,(home_points,home_last_5_points,home_goal_diff,home_progressive_carries,home_progressive_passes,home_xg,previous_away_xg,away_points,away_last_5_points,away_goal_diff,away_progressive_carries,away_progressive_passes,away_xg,previous_home_xg,home_goals_in_game,away_goals_in_game))
    outcome_db_connection.commit()


insert_columns()
insert_outcome()

