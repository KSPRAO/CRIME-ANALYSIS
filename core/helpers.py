def validate_inputs(state, year, df):
    if state in df['STATE/UT'].unique() and 2001 <= int(year) <= 2012:
        return True
    return False