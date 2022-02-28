## Imports
from lib2to3.pytree import convert
import urllib
import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime

#data
coinbase_users = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/eikona/main/coinbase_users.csv")
pokemongo_users = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/eikona/main/pg_users.csv")

st.title('Eikona Model')
st.header('Early Prototype')

col1, col2 = st.columns(2)

with col1:
    cb_historic_rate = ((coinbase_users['Coinbase Users'][len(coinbase_users)-1]-coinbase_users['Coinbase Users'][0])/coinbase_users['Coinbase Users'][0])/8
    cb_historic_rate = str(round(cb_historic_rate*100))+" %"
    st.write('Coinbase Average Annual User Growth (2014-2021):', cb_historic_rate)
    cb_growth = st.slider('Estimated YoY Growth (%) for Coinbase Users from 2022 Onward...', -100, 1000, 100)
    cb_growth = cb_growth*0.01
    l = []
    for i in range(1,5):
        year = str(2021+i)
        cb_users = round(56*(1+cb_growth)**i)
        tup=(year, cb_users)
        l.append(tup)
    cb_projected = pd.DataFrame(l, columns=['Year','Coinbase Users'])
    coinbase_users = coinbase_users.append(cb_projected, ignore_index=True)
    l = []
    for i in coinbase_users.iterrows():
        year = datetime.strptime(str(i[1]['Year']),"%Y")
        cb_users = i[1]['Coinbase Users']
        tup=(year, cb_users)
        l.append(tup)
    coinbase_users = pd.DataFrame(l, columns=['Year','Coinbase Users'])
    coinbase_users = coinbase_users.set_index('Year')


    st.subheader('Coinbase Users (in millions)')
    st.line_chart(coinbase_users)

with col2:
    pg_historic_rate = ((pokemongo_users['PG Users'][len(pokemongo_users)-1]-pokemongo_users['PG Users'][1])/pokemongo_users['PG Users'][1])/4
    pg_historic_rate = str(round(pg_historic_rate*100))+" %"
    st.write('Pokemon Go Average Annual User Growth (2017-2020):', pg_historic_rate)
    pg_growth = st.slider('Estimated YoY Growth (%) for Pokemon Go Users from 2021 Onward...', -100, 1000, 40)
    pg_growth = pg_growth*0.01
    l = []
    for i in range(1,6):
        year = str(2020+i)
        pg_users = round(166*(1+pg_growth)**i)
        tup=(year, pg_users)
        l.append(tup)
    pg_projected = pd.DataFrame(l, columns=['Year','PG Users'])
    pokemongo_users = pokemongo_users.append(pg_projected, ignore_index=True)
    l = []
    for i in pokemongo_users.iterrows():
        year = datetime.strptime(str(i[1]['Year']),"%Y")
        pg_users = i[1]['PG Users']
        tup=(year, pg_users)
        l.append(tup)
    pokemongo_users = pd.DataFrame(l, columns=['Year','PG Users'])
    pokemongo_users = pokemongo_users.set_index('Year')
    
    st.subheader('Pokemon Go Users (in millions)')
    st.line_chart(pokemongo_users)

st.subheader('Estimated Users in NFT Space')

st.header('Eikona Financial Projections: Early and Terminal')
st.subheader('Eikona early projections, starting with an estimated 1000 core users by end of 2022...')
col3, col4 = st.columns(2)
with col3:
    eikona_growth = st.slider('Estimate YoY Growth (%) for Eikona Users from 2023 to 2025', 0, 1000, 500)
    eikona_growth = eikona_growth*0.01
    l = []
    for i in range(0,4):
        year = datetime.strptime(str(2022+i),"%Y")
        eikona_users = 1000*(1+eikona_growth)**i
        tup=(year, eikona_users)
        l.append(tup)
    eikona_projected = pd.DataFrame(l, columns=['Year','Projected Eikona Users'])
    eikona_projected = eikona_projected.set_index('Year')

    st.subheader('Projected Eikona Users')
    st.line_chart(eikona_projected)

with col4:
    st.subheader('Toggle Estimates for Revenue and Costs')
    cost_mint = st.slider('Estimated Cost of User to Mint ($)...', 0.00, 5.00, 0.25, 0.25)
    server_cost = st.slider('Estimated Server Costs (Per User in $)...', 0.00, 1.00, 0.10, 0.01)
    price_mint = st.slider('Estimated Price for User to Mint ($)...', 0.00, 10.00, 5.00, 0.25)
    conversion_rate = st.slider('Estimated Share of Users Who Mint (%)...', 0, 100, 50)
    conversion_rate = conversion_rate*0.01
    ar_ad_cpm = st.slider('Estimated Avg Number of Additional Mints (Adventures) Per Converted User', 0, 50, 10)

eikona_projected = eikona_projected.reset_index()
l = []
for i in eikona_projected.iterrows():
    year = i[1]['Year']
    converts = round(i[1]['Projected Eikona Users']*conversion_rate)
    cost = (server_cost*eikona_users)+(cost_mint*converts) + (converts*ar_ad_cpm*cost_mint) + (server_cost*converts*ar_ad_cpm)
    revenue = converts*price_mint + (converts*ar_ad_cpm*price_mint)
    profit = revenue - cost
    #revenue = '${:,}'.format(float(round(converts*price_mint)))
    #profit = '${:,}'.format(float(round(profit)))
    tup=(year,converts, cost, revenue, profit)
    l.append(tup)
eikona_finances = pd.DataFrame(l, columns=['Year','Converts','Costs', 'Revenue', 'Profit'])

st.subheader('Early Financial Performance')
col5, col6 = st.columns(2)
with col5:
    eikona_finances
with col6:
    eikona_finances_graph = eikona_finances[['Year','Revenue', 'Costs', 'Profit']]
    eikona_finances_graph = eikona_finances_graph.set_index('Year')
    st.line_chart(eikona_finances_graph)
