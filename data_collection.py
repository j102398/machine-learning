#Import relevant libraries
import sqlite3

#Specify the database created , we want to fill out the outcome table manually
pathToFile = "C:\\Users\\joe\\PycharmProjects\\predictions\\predictions_archive\\predictions_gw28.db"

#Connect to the previous database
previous_db_connection = sqlite3.connect(pathToFile)
previous_db_cursor = previous_db_connection.cursor()

#We are going to put the data in a new database
new_db_connection = sqlite3.connect('data.db')
new_db_cursor = new_db_connection.cursor()



#Retrieve the list of fixtures
previous_db_cursor.execute('SELECT fixture FROM comparisons')
fixture_list = previous_db_cursor.fetchall()

#Insert an outcome table to the previous database
if False != False:

    previous_db_cursor.execute('ALTER TABLE statistics ADD COLUMN home_goals INTEGER')
    previous_db_cursor.execute('ALTER TABLE statistics ADD COLUMN away_goals INTEGER')


#Obtain outcome from fixture list
for fixture in fixture_list:
    home_goals = input(f"Enter total home goals scored in {fixture}")
    away_goals = input(f"Enter total away goals scored in {fixture}")


    #Get the home team and away team from the fixture
    home_team, away_team = fixture[0].split(' vs ')

    #Insert into the database
    query = "UPDATE  statistics  SET home_goals = ?,away_goals = ? WHERE home_team = ? AND  away_team = ?"
    previous_db_cursor.execute(query,(home_goals,away_goals,home_team,away_team,))
    previous_db_connection.commit()

#Insert all the data into the new database

def create_table():
    new_db_cursor.execute('CREATE TABLE IF NOT EXISTS data ('
                          'previous_xg REAL, '
                          'points INTEGER, '
                          'last_5_points INTEGER, '
                          'goal_diff INTEGER, '
                          'progressive_carries INTEGER, '
                          'progressive_passes INTEGER, '
                          'xg REAL,'
                          'goals_scored_in_game INTEGER)')


def insert_data():
    # For the home team:
    previous_db_cursor.execute('SELECT away_previous_xg, home_points, home_last_5_points, home_goal_diff, home_progressive_carries, home_progressive_passes, home_xg, home_goals FROM statistics')
    home_data = previous_db_cursor.fetchall()

    # Insert home team data
    for row in home_data:
        previous_xg, points, last_5_points, goal_diff, progressive_carries, progressive_passes, xg, goals_scored = row
        new_db_cursor.execute(
            'INSERT INTO data (previous_xg, points, last_5_points, goal_diff, progressive_carries, progressive_passes, xg, goals_scored_in_game) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (previous_xg, points, last_5_points, goal_diff, progressive_carries,
             progressive_passes, xg, goals_scored))

    # For the away team:
    previous_db_cursor.execute('SELECT home_previous_xg, away_points, away_last_5_points, away_goal_diff, away_progressive_carries, away_progressive_passes, away_xg, away_goals FROM statistics')
    away_data = previous_db_cursor.fetchall()

    # Insert away team data
    for row in away_data:
        previous_xg, points, last_5_points, goal_diff, progressive_carries, progressive_passes, xg, goals_scored = row
        new_db_cursor.execute(
            'INSERT INTO data (previous_xg, points, last_5_points, goal_diff, progressive_carries, progressive_passes, xg, goals_scored_in_game) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (previous_xg, points, last_5_points, goal_diff, progressive_carries,
             progressive_passes, xg, goals_scored))

    #Make sure to commit otherwise it wont save
    new_db_connection.commit()


create_table()
insert_data()
