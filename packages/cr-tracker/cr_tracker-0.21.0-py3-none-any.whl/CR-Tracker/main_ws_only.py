import pandas as pd
import numpy as np
from datetime import date,timedelta

from wsimple.api import Wsimple
def get_otp():
    return input("Enter otpnumber: \n>>>")

def Wsimple_data(email, password):
    ws = Wsimple(email, password, otp_callback=get_otp)
    df = pd.DataFrame(ws.get_activities(limit=99, type=['deposit', 'withdrawal'])['results'])
    df_value = df.value.dropna().apply(pd.Series)
    df1 = df[df.object == 'deposit'][
        ['account_id', 'object', 'created_at', 'updated_at', 'accepted_at', 'status', 'value', 'instant_value']]

    df1 = pd.concat([df1, df_value], axis=1)
    df1['Year'] = pd.to_datetime(df1['created_at']).dt.year
    df2 = df1.loc[:, ['Year', 'object', 'amount']]
    ### Create a new Column called type
    df2.loc[:, 'type'] = np.where(df2.object == 'deposit', 'Deposits', 'Withdrawals')
    df3 = df2.groupby(['Year', 'type'])['amount'].sum().rename('netAmount').reset_index()
    return df3

def create_date_list(start,end):
    date_range=pd.date_range(start, end, freq='M',)
    print(date_range)
    return date_range

def contr_start_year(birthyear=1990):
    contr_start_year=2009
    year_18=birthyear+18
    if year_18>2009:
        contr_start_year=year_18
    return contr_start_year

TFSA_dollar_limit_dict={2009:5000
,2010:5000
,2011:5000
,2012:5000
,2013:5500
,2014:5500
,2015:10000
,2016:5500
,2017:5500
,2018:5500
,2019:6000
,2020:6000
,2021:6000
,2022:6000
,2023:6500
,2024:7000
,2025:7000
,2026:7000
,2027:7000
,2028:7000
}

df_TFSA_limit=pd.DataFrame(TFSA_dollar_limit_dict.items(),columns=['year','limit'])

#Create this function so that the user can return a dataframe with the TFSA limit from every year
def df_tfsa_limit():
    df_tfsa_limit=pd.DataFrame(TFSA_dollar_limit_dict.items(),columns=['year','limit'])
    return df_tfsa_limit

##Need a function that gets your contribution room based on your birthyear
def max_contr_room_Limit(birthyear=1900,end_yr=date.today().year):
    start_year=contr_start_year(birthyear)
    limit=df_TFSA_limit[(df_TFSA_limit.year>=start_year) & (df_TFSA_limit.year<=end_yr)]['limit'].sum()
    return limit

def print_summary(df):
    today = date.today()
    current_contr_room = df.loc[df['Year'] == today.year].Current_Contr_Room.values[0]
    next_year_contr_room = df.loc[df['Year'] == today.year + 1].Current_Contr_Room.values[0]
    print("Today's date:", today)
    print(f"Your current contribution room is: ${current_contr_room}")
    print(f"Next Year's Contribution room on Jan 1 {today.year + 1} is:  ${next_year_contr_room}")
    return  current_contr_room,next_year_contr_room


# Add optional arguments here
## given is the contribution room and year from the CRA
def contribution_room(email, password, given_year=None, given_contr_room=None, open_year=2009, birth_year=1990):
    contr_start_year1 = contr_start_year(birth_year)

    if given_year is None or given_contr_room is None:
        given_year = None
        given_contr_room = None

    if given_year != None:
        start_year = given_year
        start_contr_room = given_contr_room
    # If they inputted a valid open_year use the open year
    elif open_year >= 2009:
        start_year = open_year
        start_contr_room = max_contr_room_Limit(birth_year, start_year)
    # If the user did not input anything assume they are were born before 1990
    ## and start year is 2009
    else:
        start_year = contr_start_year1
        start_contr_room = max_contr_room_Limit(birth_year, start_year)

    print(f'start_year is {start_year}')
    #Raise error if start year is before 2009 or After the current year
    if (start_year < 2009) or (start_year > date.today().year):
        raise Exception('given year or open year is not Valid!')

    ### Get the data with create_df
    if start_year == 2009:
        print('WARNING: A valid year was not input as open_year or given_year. THIS WILL TAKE A VERY LONG TIME.')
    df = Wsimple_data(email, password)
    ### filter df so that it only has value after the start_year, since we can't control the date range from the ws api
    df_filtered = df[df.Year >= start_year]

    df1 = df_filtered.groupby(['Year', 'type'])['netAmount'].sum().reset_index()
    ## Append the Wealthsimple data here
    # if not df_ws.empty:
    #     df1 = pd.concat([df1, df_ws], axis=0, ignore_index=True)

    df2 = df1.pivot_table(index='Year', columns='type', values='netAmount').reset_index()
    # If Deposits or withdrawals don't exist add it now
    df2.loc[:, 'Deposits'] = df2.get('Deposits', 0)
    df2.loc[:, 'Withdrawals'] = df2.get('Withdrawals', 0)

    # first thing is limit the df to the year that was given
    df3 = df2.reset_index(drop=True)

    # Insert enough rows so that there is one row for every year until next year
    # this will fix if they had no activity in a year.
    b = pd.DataFrame({'Year': [x for x in range(start_year, date.today().year + 2)]})
    df4 = pd.merge(left=df3, right=b, on='Year', how='outer').fillna(0).sort_values(by='Year').reset_index(drop=True)

    # Add the Given Contribution Room on January 1st
    # first make a new column with zeros
    df4.insert(0, 'Contr_Room_Jan1', 0)
    # Update the value in one cell
    # TO DO need to fix this in case the given contribution room does not match the date range that you have for the dataframe
    # Update Contr room on Jan 1 to be the given value
    df4.loc[:, 'Contr_Room_Jan1'] = np.where(df4.Year == start_year, start_contr_room, df4.Contr_Room_Jan1)

    # Add a new Column 'New Year Dollar limit"
    df4.insert(0, 'New_Year_Dollar_Limit', df4['Year'].map(TFSA_dollar_limit_dict))

    # Calculate Contr Room on Jan 1
    for i in range(1, len(df4)):
        df4.loc[i, 'Contr_Room_Jan1'] = df4.loc[i - 1, 'Contr_Room_Jan1'] - df4.loc[i - 1, 'Deposits'] - df4.loc[
            i - 1, 'Withdrawals'] + df4.loc[i, 'New_Year_Dollar_Limit']

    ## Calculate the Current Contribution Room
    df4.insert(5, 'Current_Contr_Room', df4.Contr_Room_Jan1 - df4.Deposits)

    ### print summary
    current_contr_room, next_year_contr_room = print_summary(df4)

    return current_contr_room, next_year_contr_room, df4


# Create a function so that if new information is found we can just update the dataframe instead of grabbing the activity again
def update_df(df, given_year=None, given_contr_room=None, birth_year=1990):
    # contr_start_year1=contr_start_year(birth_year)
    # df1=df.copy()
    if given_year is None or given_contr_room is None:
        given_year = df.Year.min()
        given_contr_room = max_contr_room_Limit(birth_year, df.Year.min())

    # print(given_year,given_contr_room)
    df.loc[:, 'Contr_Room_Jan1'] = np.where(df.Year == given_year, given_contr_room, df.Contr_Room_Jan1)

    # Calculate Contr Room on Jan 1
    ### Only update the rows after given_year, so start the range with the index after given_year
    ### If we update all rows, it will overwrite the change we just made above
    for i in range(dfa[dfa.Year == given_year].index[0] + 1, len(df)):
        df.loc[i, 'Contr_Room_Jan1'] = df.loc[i - 1, 'Contr_Room_Jan1'] - df.loc[i - 1, 'Deposits'] - df.loc[
            i - 1, 'Withdrawals'] + df.loc[i, 'New_Year_Dollar_Limit']

    ## Calculate the Current Contribution Room
    df.loc[:, 'Current_Contr_Room'] = df.Contr_Room_Jan1 - df.Deposits

    return df