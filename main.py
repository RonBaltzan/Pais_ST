import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np

#function to load data
#input: path to PKL format
#output: data frame

def Load(path):
    df = pd.read_pickle(path)
    return df

#Loading number selection GUI
def sel_num():
    list_num = list(np.arange(1, 37, 1)) #list for regular numbers
    list_strong = list(np.arange(1, 8, 1)) #list for strong number
    numbers = st.multiselect('**Enter regular numbers**', list_num, max_selections=6)
    extra = st.multiselect('**Enter strong number**', list_strong, max_selections=1)

    return [numbers, extra]

if __name__ == '__main__':
    print('start')

    # Finding if prize won in ballot
    # input:
    # l_gus: [[6 no.],[strong no.]] #guess
    # l_won: [[6 no.],[strong no.]] #winning no.
    # df_ball: ballot data
    # output:
    # [#prize no., prize sum]
    
    def i_won(l_gus, l_won, df_ball):
        # checking how many regular no.gueesed
        res = list(np.isin(l_gus[0], l_won[0]))  # comparing guess to actual no.
        # checking right guessed
        count = 0
        for x in res:
            if str(x) == 'True':
                count = count + 1
        guess = str(count)  # num of right resular numbers guessed
        # checking extra no.
        if l_gus[1][0] == l_won[1]:
            guess = guess + 'חזק'  # building guess
        # checking which prize won
        for i, pla in enumerate((df_ball['Guess type'])):
            if (guess == pla or guess[0] == str(pla)):
                prz_no = df_ball.loc[i, 'Prize No.']  # getting prize sum
                prz_sum = df_ball.loc[i, 'Prize sum [NIS]']  # getting prize sum
                break
            else:
                prz_no = 0  # getting prize sum
                prz_sum = 0  # getting prize sum
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
        #calculating total sum
        df1['Total sum'] = ""
        t_price = 6 #ticket price
        for i, s in enumerate(df1['Prize sum']):
            if i==0:
                df1.loc[i, 'Total sum'] = (s - t_price)
            else:
                tmp = s-t_price+df1.loc[i-1, 'Total sum']
                df1.loc[i, 'Total sum'] = tmp
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
    data = Load('data_20230730.pkl') #load data base
    m_title = '<p style="font-family:sans-serif;text-align: center; color:Blue; font-size: 48px;">Could You Be a Milionare?</p>'
    st.markdown(m_title, unsafe_allow_html=True)
    m_title = '<p style="font-family:sans-serif;text-align: center; color:Blue; font-size: 18px;">[Based on real results of over 2500 ballots]</p>'
    st.markdown(m_title, unsafe_allow_html=True)
    #Enter numbers
    Reg_num = st.multiselect('**Enter regular numbers**', list(np.arange(1, 37, 1)), max_selections=6)     #regular numbers
    if len(Reg_num) == 6:
        extra = st.multiselect('**Enter strong number**',list(np.arange(1, 8, 1)), max_selections=1)
    if (len(Reg_num) == 6 and len(extra) == 1): #when input completed
        num= [Reg_num, extra]
        res = check(num, data) #check results for input
        st.balloons()
        db_highest = res[res['Prize sum'] == res['Prize sum'].max()].reset_index() #finding hightest prize won
        #Printing highest prize won
        high = num_format(db_highest.loc[0, 'Prize sum'])+ u"\u20AA" #Building string
        p_title = f'<p style="font-family:sans-serif; color:Green; font-size: 24px;">Highest Single Prize won: {high} </p>' #define text
        st.markdown(p_title, unsafe_allow_html=True) #create markdowm
        # Printing highest ballot data for max win
        ballot1 = str(db_highest.loc[0, 'Prize no.']) # Building string
        ballot2 = str(db_highest.loc[0, 'Ballot No.'])
        ballot3 = str(db_highest.loc[0, 'Date'])
        b_title = f'<p style="font-family:sans-serif; color:Orange; font-size: 14px;">[Prize no. {ballot1}  at Ballot no. {ballot2} ({ballot3})]</p>'  # define text
        st.markdown(b_title , unsafe_allow_html=True)  # create markdowm
        #calculating parameteres
        res_title = f'<p style="font-family:sans-serif;font-weight:bold; text-decoration: underline;  color:Grey; font-size: 16px;">Summary of Total Results: </p>'  # define text
        st.markdown(res_title, unsafe_allow_html=True)  # create markdowm
        rev = sum(res['Prize sum']) # revnue
        inv = len(data) * 6  #  investment
        earn = rev - inv  # earnings
        # Printing highest total winning sum
        rev = num_format(rev) #formating
        rev = str(rev + u"\u20AA")
        r_title = f'<p style="font-family:sans-serif;font-weight:bold;  color:Orange; font-size: 16px;">Winnings Total: {rev} </p>'  # define text
        st.markdown(r_title, unsafe_allow_html=True)  # create markdowm
        # Printing highest totalinvetment sum
        inv = num_format(inv) #formating
        inv = str(inv + u"\u20AA")
        i_title = f'<p style="font-family:sans-serif;font-weight:bold;  color:Orange; font-size: 16px;">Investment Total (6 \u20AA per ballot): {inv} </p>'  # define text
        st.markdown(i_title, unsafe_allow_html=True)  # create markdowm
        # Printing highest total winning sum
        earn = num_format(earn)  # formating
        earn = str(earn + u"\u20AA")
        e_title = f'<p style="font-family:sans-serif;font-weight:bold; text-align: center; color:Red; font-size: 24px;">Earning\Losing Total: {earn} </p>'  # define text
        st.markdown(e_title, unsafe_allow_html=True)  # create markdowm
        #ploting
        sp_data = Load('SP500.pkl') #load data base
        # S&P title
        sp_tot = str(int(np.round(sp_data[1][len(sp_data[1])-1],0))) #finding total sum from S&P investment
        sp_tot= num_format(sp_tot) #change format
        sp_tot = sp_tot + u"\u20AA"
        sp_title = f'<p style="font-family:sans-serif;font-weight:bold; text-align: center; color:Grey; font-size: 18px;">If you would have invest instead in S&P 500, you could have: {sp_tot} </p>'  # define text
        st.markdown(sp_title, unsafe_allow_html=True)  # create markdowm
        #plot
        #S&P 500 chart
        res['Date'] = pd.to_datetime(res['Date'], format='%d/%m/%Y').dt.strftime('%Y') #change format
        fig = go.Figure()
        #S&P plot
        fig.add_trace(go.Scatter(x=sp_data[0],y=sp_data[1],
                                 mode='lines',
                                 name='S&P 500'))
        #Lotto plot
        fig.add_trace(go.Line(x=res['Date'], y=res['Total sum'],
                                 mode='lines',
                                 name='Lotto', fillcolor= 'Black'))
        fig.update_layout(title="Comparasion between investing same amount in Lotto or S&P 500", xaxis_title="Date",
                          yaxis_title="Profit \ Loss [\u20AA]")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
