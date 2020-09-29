"""Calculate Stats"""


# Add Field Independent Pitching Stat
def add_fip(df):
    df['FIP'] = (((13 * df['HR_P']) + (3 * (df['BB_P'] + df['HBP_P'])) - (2 * df['SO_P'])) / df['innings_pitched']) +\
                3.1
    return df


# Adds Matchups Between Pitcher and Hitter
def add_matchups(df):
    df['matchup'] = df['bat_id'] + '_' + df['pit_id'] + '_' + df['year']
    df['matchup_ct'] = df.groupby('matchup').cumcount() + 1
    df['matchup_ct'].fillna(value=0, inplace=True)
    df.drop('matchup', 1, inplace=True)
    return df


def add_year_label(df):
    df['year'] = df['game_id'].str[3:7]
    df['year'] = df['year'].astype('str')
    return df


def add_dominant_arm(df):
    df['dominant'] = df['pit_hand_cd'] + df['bat_hand_cd']
    return df


def assign_hit_bins(hits):
    if hits < 150:
        return 1
    if 150 <= hits <= 169:
        return 2
    if 170 <= hits <= 189:
        return 3
    if 190 <= hits <= 209:
        return 4
    if hits >= 210:
        return 5


def assign_hit_event_bins(hit_event):
    if hit_event < 0.05:
        return 1
    if 0.05 <= hit_event < 0.10:
        return 2
    if 0.10 <= hit_event < 0.15:
        return 3
    if 0.15 <= hit_event < 0.20:
        return 4
    if hit_event >= 0.20:
        return 5


# Hits Allowed per Game
def add_h_a_per_game(df):
    df['ha_pg'] = df['H_P'] / df['G_P']
    return df


# Batter Hits per Game
def add_hits_per_game(df):
    df['bh_pg'] = df['H'] / df['G']
    return df


# Pitcher Strike Outs per Game
def add_so_per_game(df):
    df['so_pg'] = df['SO_P'] / df['G_P']
    return df


# Batter Singles
def add_bat_singles(df):
    df['singles'] = df['H'] - (df['doubles'] + df['triples'] + df['HR'])
    return df


'''Log5 Probabilities'''


# Batter Single
def add_single_log5(df):
    df['prob1'] = df['singles'] / df['AB']
    return df


# Batter Double
def add_double_log5(df):
    df['prob2'] = df['doubles'] / df['AB']
    return df


# Batter Triple
def add_triple_log5(df):
    df['prob3'] = df['triples'] / df['AB']
    return df


# Batter HR
def add_hr_log5(df):
    df['prob4'] = df['HR'] / df['AB']
    return df


# Pitcher Single
def add_psingle_log5(df):
    df['p_prob1'] = df['singles_a'] / df['batters_faced']
    return df


# Pitcher Double
def add_pdouble_log5(df):
    df['p_prob2'] = df['doubles_a'] / df['batters_faced']
    return df


# Pitcher Triple
def add_ptriple_log5(df):
    df['p_prob3'] = df['triples_a'] / df['batters_faced']
    return df


# Pitcher HR
def add_phr_log5(df):
    df['p_prob4'] = df['HR_P'] / df['batters_faced']
    return df


# Pitcher/Batter HR Event
def add_pbhr_event(df):
    df['hr_event'] = ((df['prob4'] * df['p_prob4']) / 0.025504387009178134) / (2 + ((1-df['prob4'])*(1-df['p_prob4']))/(
            1-0.025504387009178134))
    return df


# Pitcher/Batter Single Event
def add_pbs_event(df):
    df['s_event'] = ((df['prob1'] * df['p_prob1']) / 0.1500271988435895) / (2 + ((1-df['prob1'])*(1-df[
        'p_prob1']))/(
            1-0.1500271988435895))
    return df


# Pitcher/Batter Double Event
def add_pbd_event(df):
    df['d_event'] = ((df['prob2'] * df['p_prob2']) / 0.04547155361704142) / (2 + ((1-df['prob2'])*(1-df[
        'p_prob2']))/(
            1-0.04547155361704142))
    return df


# Pitcher/Batter Triple Event
def add_pbt_event(df):
    df['t_event'] = ((df['prob3'] * df['p_prob3']) / 0.004286145561218607) / (2 + ((1-df['prob3'])*(1-df['p_prob3']))/(
            1-0.004286145561218607))
    return df


# Pitcher/Batter Hit Event
def add_hit_event(df):
    df['hit_event'] = df['s_event'] + df['d_event'] + df['t_event'] + df['hr_event']
    return df




