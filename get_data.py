"""
Pull Data from Lahman Database
    & Combine Event Files
"""
import glob
import pandas as pd


# Query to Pull Pitching Data
pitching_query = '''
            SELECT sum(pitching.ER) AS "earned_runs",
                sum(pitching.IPouts) / 3 AS "innings_pitched",
                sum(pitching.H) AS "H_P",
                sum(pitching.SO) AS "SO_P",
                sum(pitching.ERA) AS "ERA",
                sum(pitching.BFP) AS "batters_faced",
                sum(pitching.BAOpp) AS "Opp_BA",
                sum(pitching.BB) AS "BB_P",
                sum(pitching.HR) AS "HR_P",
                sum(pitching.HBP) AS "HBP_P",
                sum(pitching.G) AS "G_P",
                master.throws AS "throwing_arm",
                master.retroID AS "pit_id",
                pitching.yearID AS "year"
            FROM pitching INNER JOIN master ON pitching.playerID = master.playerID
            WHERE pitching.yearID >= '2012' AND (pitching.IPouts / 3) >= 162
            GROUP BY master.throws, 
                master.retroID,
                pitching.yearID;'''


# Query to Pull Batting Data
batting_query = '''
            SELECT sum(batting.H) AS "H",
                sum(batting.SO) AS "SO",
                sum(batting.doubles) AS "doubles",
                sum(batting.triples) AS "triples",
                sum(batting.HR) AS "HR",
                sum(batting.AB) AS "AB",
                sum(batting.BB) AS "BB",
                sum(batting.HBP) AS "HBP",
                sum(batting.SF) AS "SF",
                sum(batting.G) AS "G",
                master.bats AS "batter_arm",
                master.retroID AS "bat_id",
                batting.yearID AS "year"
            FROM batting INNER JOIN master ON batting.playerID = master.playerID
            WHERE batting.yearID >= '2012' AND batting.AB >= 502
            GROUP BY master.bats,
                master.retroID,
                batting.yearID;'''


# Combine Event*.csv Files
def get_events():
    df = pd.DataFrame()
    cols = ['game_id', 'inn_ct', 'balls_ct', 'strikes_ct', 'bat_id', 'bat_hand_cd', 'pit_id', 'pit_hand_cd', 'h_fl',
            'EVENT_OUTS_CT', 'RBI_CT', 'EVENT_CD']
    for i, file in enumerate(glob.glob('Event*.csv')):
        print(file)
        tmp_df = pd.read_csv(file, usecols=cols)
        df = df.append(tmp_df)
    df.columns = map(str.lower, df.columns)
    return df




