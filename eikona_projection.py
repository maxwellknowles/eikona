## Imports
import urllib 
import pandas as pd
import streamlit as st
import numpy as np

#data
coinbase_users = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/eikona/main/coinbase_users.csv")
pokemongo_users = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/eikona/main/pg_users.csv")

st.title('Eikona Model')
st.header('Early Prototype')

col1, col2, col3 = st.columns(3)

with col1:
    cb_growth = st.slider('Estimated YoY Growth (%) for Coinbase Users...', -10, 100, 1)
    cb_growth = cb_growth*0.01
    l = []
    for i in range(1,5):
        year = 2021+i
        cb_users = 56*(1+cb_growth)**i
        tup=(year, cb_users)
        l.append(tup)
    cb_projected = pd.DataFrame(l, columns=['Year','Coinbase Users'])
    coinbase_users = coinbase_users.append(cb_projected, ignore_index=True)
    coinbase_users = coinbase_users.set_index('Year')

    st.subheader('Coinbase Users (in millions)')
    st.line_chart(coinbase_users)

with col2:
    pg_growth = st.slider('Estimated YoY Growth (%) for Pokemon Go Users...', -10, 100, 1)
    pg_growth = pg_growth*0.01
    m = []
    for i in range(1,6):
        year = 2020+i
        pg_users = 166*(1+pg_growth)**i
        tup=(year, pg_users)
        m.append(tup)
    pg_projected = pd.DataFrame(m, columns=['Year','PG Users'])
    pokemongo_users = pokemongo_users.append(pg_projected, ignore_index=True)
    pokemongo_users = pokemongo_users.set_index('Year')
    
    st.subheader('Pokemon Go Users (in millions)')
    st.line_chart(pokemongo_users)

with col3:
    eikona_growth = st.slider('Estimated YoY Growth (%) for Eikona Users...', 0, 1000, 10)
    eikona_growth = eikona_growth*0.01
    l = []
    for i in range(1,5):
        year = 2021+i
        eikona_users = 1000*(1+eikona_growth)**i
        tup=(year, eikona_users)
        l.append(tup)
    eikona_projected = pd.DataFrame(l, columns=['Year','Projected Eikona Users'])
    eikona_projected = eikona_projected.set_index('Year')

    st.subheader('Projected Eikona Users')
    st.line_chart(eikona_projected)
    
st.subheader('Financial Projections')   
cost_mint = st.slider('Estimated Cost of User to Mint ($)...', 0, 5, 1)
server_cost = st.slider('Estimated Server Costs (Per User in $)...', 0, 10, 1)
price_mint = st.slider('Estimated Price for User to Mint ($)...', 0, 10, 1)
conversion_rate = st.slider('Estimated Share of Users Who Mint (%)...', 0, 100, 1)
conversion_rate = conversion_rate*0.01
eikona_projected = eikona_projected.reset_index()
l = []
for i in eikona_projected.iterrows():
    year = str(i[1]['Year'])
    converts = round(i[1]['Projected Eikona Users']*conversion_rate)
    cost = (server_cost*eikona_users)+(cost_mint*converts)
    revenue = converts*price_mint
    profit = revenue - cost
    tup=(year,converts, cost, revenue, profit)
    l.append(tup)
eikona_finances = pd.DataFrame(l, columns=['Year','Converts','Costs', 'Revenue', 'Profit'])
eikona_finances
eikona_finances_graph = eikona_finances[['Year','Revenue','Profit']]
eikona_finances_graph = eikona_finances_graph.set_index('Year')
st.line_chart(eikona_finances_graph)
