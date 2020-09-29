"""
Pull Data from Lahman Database
    & Combine Event Files
"""
import glob
import pandas as pd


# Query to Pull Pitching Data
pitching_query = '''
            select sum(pitching.ER) as "earned_runs",
                sum(pitching.IPouts) / 3 as "innings_pitched",
                sum(pitching.H) as "H_P",
                sum(pitching.SO) as "SO_P",
                sum(pitching.ERA) as "ERA",
                sum(pitching.BFP) as "batters_faced",
                sum(pitching.BAOpp) as "Opp_BA",
                sum(pitching.BB) as "BB_P",
                sum(pitching.HR) as "HR_P",
                sum(pitching.HBP) as "HBP_P",
                sum(pitching.G) as "G_P",
                master.throws as "throwing_arm",
                master.retroID as "pit_id",
                pitching.yearID as "year"
            from pitching inner join master on pitching.playerID = master.playerID
            where pitching.yearID >= '2012' and (pitching.IPouts / 3) >= 162
            group by master.throws, 
                master.retroID,
                pitching.yearID;'''


# Query to Pull Batting Data
batting_query = '''
            select sum(batting.H) as "H",
                sum(batting.SO) as "SO",
                sum(batting.doubles) as "doubles",
                sum(batting.triples) as "triples",
                sum(batting.HR) as "HR",
                sum(batting.AB) as "AB",
                sum(batting.BB) as "BB",
                sum(batting.HBP) as "HBP",
                sum(batting.SF) as "SF",
                sum(batting.G) as "G",
                master.bats as "batter_arm",
                master.retroID as "bat_id",
                batting.yearID as "year"
            from batting inner join master on batting.playerID = master.playerID
            where batting.yearID >= '2012' and batting.AB >= 502
            group by master.bats,
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




