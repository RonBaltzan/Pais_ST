import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

#function to load data
#input: path to PKL format
#output: data frame

def Load(path):
    df = pd.read_pickle(path)
    return df

def sel_num():
    list_num = list(np.arange(1, 37, 1))
    list_strong = list(np.arange(1, 8, 1))
    numbers = st.multiselect('**Enter regular numbers**', list_num, max_selections=6)
    extra = st.multiselect('**Enter strong number**', list_strong, max_selections=1)

    return [numbers, extra]
    
if __name__ == '__main__':
    print('Loading)

    # Finding if prize won in ballot
    # input:
    # l_gus: [[6 no.],[strong no.]] #guess
    # l_won: [[6 no.],[strong no.]] #winning no.
    # df_ball: ballot data
    # output:
    # [#prize no., prize sum]
    import numpy as np


    def i_won(l_gus, l_won, df_ball):
        # checking how many regular no.gueesed
        res = list(np.isin(l_gus[0], l_won[0]))  # comparing guess to actual no.
        # checking right guessed
        count = 0  # counter for right guessed
        for v in res:
            if v == True:
                count = count + 1
        # checking extra no.
        # if won
        if l_gus[1][0] == l_won[1]:
            guess = str(count) + 'חזק'  # building guess
        else:
            guess = str(count)
        # checking what prize won
        # convert guess type column to constant format (to avoid error)
        df_ball['Guess type'] = df_ball['Guess type'].apply(lambda x: x.replace(' ', '').replace('+', ''))
        # fixing table order (avoid error in some tables)
        df_ball = df_ball.sort_values('Prize sum [NIS]', ascending=False).reset_index(drop=True)
        df_ball['Prize No.'] = np.arange(1, len(df_ball) + 1, 1)
        # checking which prize won
        for j, p in enumerate(df_ball['Guess type']):
            # if there is a match (prize won)
            if p in guess:
                prz_no = df_ball.loc[j, 'Prize No.']  # getting prize sum
                prz_sum = df_ball.loc[j, 'Prize sum [NIS]']  # getting prize sum
                # in case no winners
                if prz_sum == 0:
                    prz_sum = df_ball.loc[j, 'Total prize sum [NIS]']  # getting total prize sum
                break
            # if  no. no guess
            else:
                prz_sum = 0
                prz_no = 0

        return [prz_no, prz_sum]


    # function to check ballot summary for given guess
    # Input:
    # guess: [[6 numbers], strong number]
    # db : ballot database
    # Output:
    # results: dataframe

    def check(guess, db):
        df1 = pd.DataFrame(columns=['Ballot No.', 'Date', 'Winning no.', 'Prize no.', 'Prize sum'])
        for i in range(len(db)):
            [p_num, p_sum] = i_won(guess, db.loc[i, 'Winning numbers'], db.loc[i, 'Prizes data'])  # getting current prize sum
            df1.loc[len(df1)] = [db.loc[i, 'Ballot no.'], db.loc[i, 'Date'], db.loc[i, 'Winning numbers'], p_num, p_sum]
        return df1

    #function to format numbers with ','
    #input: number
    #output: formated no.
    def num_format(number):
        l = []
        num = str(number)
        tmp = ''
        for i in range(len(num) - 1, -1, -1):
            #in case there is a negative number
            if num[i] == '-':
                break
            tmp = num[i] + tmp
            if len(tmp) == 3:
                l.append(tmp)
                tmp = ''
        if len(tmp) > 0:
            l.append(tmp)
        mod_num = (',').join(l[::-1])
        # in case there is a negative number
        if num[i] == '-':
            mod_num = '-'+mod_num
        return mod_num
###########################################
#running code
    m_title = '<p style="font-family:sans-serif;text-align: center; color:Blue; font-size: 48px;">Could You Be a Milionare?</p>'
    st.markdown(m_title, unsafe_allow_html=True)
    num = sel_num() #load streamlit numbers selector
    data = Load(r'https://github.com/RonBaltzan/Pais_ST/blob/main/data_20230726.pkl') #load data base
    if len(num[0]) == 6 and len(num[1]) == 1: #when input completed
        res = check(num, data) #check results for input
        db_highest = res[res['Prize sum'] == res['Prize sum'].max()].reset_index() #finding hightest prize won
        #Printing highest prize won
        high = num_format(db_highest.loc[0, 'Prize sum'])+ u"\u20AA" #Building string
        p_title = f'<p style="font-family:sans-serif; color:Green; font-size: 24px;">Highest Single Prize won: {high} </p>' #define text
        st.markdown(p_title, unsafe_allow_html=True) #create markdowm
        # Printing highest ballot data for max win
        ballot1 = str(db_highest.loc[0, 'Prize no.']) # Building string
        ballot2 = str(db_highest.loc[0, 'Ballot No.'])
        ballot3 = str(db_highest.loc[0, 'Date'])
        b_title = f'<p style="font-family:sans-serif; color:Black; font-size: 16px;">[Prize no. {ballot1}  at Ballot no. {ballot2} ({ballot3})]</p>'  # define text
        st.markdown(b_title , unsafe_allow_html=True)  # create markdowm
        #calculating parameteres
        rev = sum(res['Prize sum']) # revnue
        inv = len(data) * 42  #  investment
        earn = rev - inv  # earnings
        # Printing highest total winning sum
        rev = num_format(rev) #formating
        rev = str(rev + u"\u20AA")
        r_title = f'<p style="font-family:sans-serif;font-weight:bold;  color:Black; font-size: 16px;">Winnings Total: {rev} </p>'  # define text
        st.markdown(r_title, unsafe_allow_html=True)  # create markdowm
        # Printing highest totalinvetment sum
        inv = num_format(inv) #formating
        inv = str(inv + u"\u20AA")
        i_title = f'<p style="font-family:sans-serif;font-weight:bold;  color:Black; font-size: 16px;">Investment Total: {inv} </p>'  # define text
        st.markdown(i_title, unsafe_allow_html=True)  # create markdowm
        # Printing highest total winning sum
        earn = num_format(earn)  # formating
        earn = str(earn + u"\u20AA")
        e_title = f'<p style="font-family:sans-serif;font-weight:bold; text-align: center; color:Red; font-size: 24px;">Earning\Losing Total: {earn} </p>'  # define text
        st.markdown(e_title, unsafe_allow_html=True)  # create markdowm
