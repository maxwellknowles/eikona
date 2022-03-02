## Imports
from audioop import avg
from lib2to3.pytree import convert
import urllib
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import urllib.request

##data
coinbase_users_historic = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/eikona/main/coinbase_users.csv")
pokemongo_users = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/eikona/main/pg_users.csv")


industry_sizes = {
  "Companies": ['TikTok', 'Facebook', 'Banks'],
  "Size": [1000000000, 2900000000, 5500000000]
}
industry_sizes = pd.DataFrame(industry_sizes)

#####
##Variables/Default values - PreCache
#####

###Calculating TPM
interval_of_users = 50
p_coefficient = float(0.03)
q_coefficient = float(0.38)

#Define Bass Diffusion Model Function first here for efficiency
def get_bass_model(p, q, M, period = 30):

    # Initializing the arrays
    A = [0] * period
    R = [0] * period
    F = [0] * period
    N = [0] * period

    # One important thing to note, is that the time period we start from is t = 0.
    # In many articles, you will see time starting from t = 1. They are both the
    # same for all intents and purposes. Starting with t = 0 makes life easier in
    # python, as indexing in python starts from 0 too.

    # We start with A(0) =0, and build up the values for t = 0 from the equations
    # formulated
    A[0] = 0
    R[0] = M
    F[0] = p
    N[0] = M*p

    # Recursion starts from next time step
    t = 1

    # Creating a helper function for recursion
    def get_bass_model_helper(A, R, F, N, t):

        # If we have reached the final period, return the values
        if t == period:
            return N, F, R, A
        else:

            # Else, just compute the values for t
            A[t] = N[t-1] + A[t-1]
            R[t] = M - A[t]
            F[t] = p + q * A[t]/M
            N[t] = F[t] * R[t]

            # compute values for the next time step
            return get_bass_model_helper(A, R, F, N, t+1)

    N, F, R, A = get_bass_model_helper(A, R, F, N, t)

    # Converting to numpy arrays and returning.
    return np.array(N), np.array(A)

###Calculating TPMS
avg_b2bsales = 3

#-------------------------
#Main Menu Sidebar -- CONFIG
#-------------------------
st.set_page_config(layout = "wide")
with st.sidebar:

    choose = option_menu("Eikona Projections", ["Other", "Business Model Projector", "Tokenomics"],
                         icons=['clipboard-data-fill'],
                         menu_icon="building", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#BBBBBD"},
        "icon": {"color": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#BBBBBD"},
    }
    )


#-------------------------
#Business Model
#-------------------------
if choose == "Business Model Projector":
    st.title('Eikona Model')
    st.header('Early Prototype')

    #-------------------------
    ###Business Model Sidebar -- CONFIG
    #-------------------------

    with st.sidebar:
        bm_sidebar = option_menu("Business Model", ["Instructions","Industry Growth", "Calculating TPM", "Estimating TPMS", "Lenz Business Models", "Flywheel", "AR Ads"],
                         icons=['bug'],
                         menu_icon="calculator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#BBBBBD"},
        "icon": {"color": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#BBBBBD"},
    }
    )
    #-------------------------
    ###Business Model Sidebar -- Industry Growth & Trends
    #-------------------------
    if bm_sidebar == "Industry Growth":
        st.title('Industry Growth & Trends')


        col1, col2 = st.columns(2)

        #################
        ###Industry Growth
        # Coinbase YoY -- millions
        ###Changeables/Sliders:
        # - Estimated YoY Growth% from 2022 Onward
        #################

        with col1:
            cb_historic_rate = ((coinbase_users_historic['Coinbase Users'][len(coinbase_users_historic)-1]-coinbase_users_historic['Coinbase Users'][0])/coinbase_users_historic['Coinbase Users'][0])/8
            cb_historic_rate = str(round(cb_historic_rate*100))+" %"
            st.write('Coinbase Average Annual User Growth (2014-2021):', cb_historic_rate)
            cb_growth = st.slider('Estimated YoY Growth (%) for Coinbase Users from 2022 Onward...', -100, 1000, 100)
            cb_growth = cb_growth*0.01
            l   = []
            for i in range(1,5):
                year = str(2021+i)
                cb_users = round(56*(1+cb_growth)**i)
                tup=(year, cb_users)
                l.append(tup)
            cb_projected = pd.DataFrame(l, columns=['Year','Coinbase Users'])
            coinbase_users = coinbase_users_historic.append(cb_projected, ignore_index=True)
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

        #################
        ###Industry Growth
        # Pokemon YoY -- millions
        ###Changeables/Sliders:
        # - Estimated YoY Growth% from 2022 Onward
        #################

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
    
    
    #-------------------------
    ###Business Model Sidebar -- Calculating TPM
    #-------------------------
    if bm_sidebar == "Calculating TPM":
        st.title('Industry Growth & Trends')

        #Setting Up Sliders
        industry_size = st.slider('Select Industry Size by 2040 (IN BILLIONS)', min_value = 0.1, max_value = 5.5,value = 1.0, step = 0.1)

        p_coefficient = st.slider('P Coefficient', min_value = 0.001, max_value = 0.05, value = p_coefficient, step = 0.005)
        q_coefficient = st.slider('P Coefficient', min_value = 0.25, max_value = 0.55, value = q_coefficient, step = 0.025)
        period = st.slider('Period of time to predict until:', min_value = 10, max_value = 100, value = 20, step = 1)

        industry_size = 1000000000 * industry_size

        #col1 = st.columns(1)
        #with col1:
        st.header('Bass Diffusion')
            #number of users, i.e. there should be a datapoint for each industry_size/interval_size


        fig = plt.figure()
        ax = plt.gca()


        #Pull in historic Coinbase user data and reformat for Bass graph
        coinbase_users_historic["Lifetime"] = coinbase_users_historic['Year']-2014
        coinbase_users_historic = coinbase_users_historic.drop("Year", 1)
        coinbase_users_historic["Users"] = coinbase_users_historic['Coinbase Users']*1000000
        coinbase_users_historic = coinbase_users_historic.drop("Coinbase Users", 1)
            #Calling the function to get the new models
        N, A = get_bass_model(p_coefficient, q_coefficient, M=float(industry_size), period = period)
            
            #Creating Periods
        t = list(range(0, period))

            #Plotting Data and changing size of points
        ax.plot(t, N, 'o', markersize = 4)

        #Plot Coinbase user data
        ax.plot(coinbase_users_historic['Lifetime'], coinbase_users_historic['Users'],'o', markersize=5)
            
            #Give it a cleaner look and remove the spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

            # Setting label and title
        ax.set_title('Adoption Count for p = {} and q = {}'.format(p_coefficient, q_coefficient))
        ax.set_ylabel("New Customers")
        ax.set_xlabel("Industry Lifetime (y)")

            # Creating a clean layout
        fig.tight_layout()

        st.pyplot(fig)



    #-------------------------
    ###Business Model Sidebar -- Estimating TPMS using Market Strategy
    #-------------------------
    if bm_sidebar == "Estimating TPMS":
        st.title('Estimating TPMS using our Marketing Strategy')
        st.header('Our default TPMS is set to xpercent of the total potential cryptocurrency market by 2040')


        avg_b2bsales = st.slider('Average number of B2B Sales per month (All get put on Lenz)', min_value = 0, max_value = 25, value = 3, step = 1)
        avg_collectionsize = st.slider('Average collection size per B2B Sale', min_value = 50, max_value = 10000, value = 1000, step = 50)
        avg_NFTsPH = st.slider('Average number of NFTs per unique owner', min_value = 1.0, max_value = 10.0, value = 3.0, step = 0.2)
        avg_HolderBase = st.slider('Average percent of Total Collection Holders that end up downloading Lenz once to try with their collection that just got partnered', min_value = 0, max_value = 100, value = 25, step = 1)

        total_reached_with_Lenz = (((float(avg_collectionsize)/avg_NFTsPH)*float(avg_b2bsales))*(float(avg_HolderBase)*0.01))
        st.header('Total # of new people reached with Lenz per month:' + str(total_reached_with_Lenz))
        st.header('-------------------------------------------------------------------------------------')


        st.header('American Cancer Society TikTok/Twitter Campaign')

        col1, col2 = st.columns(2)

        with col1:
            st.header('TikTok')
            acs_TikTok = st.number_input('American Cancer Society TikTok Following(Thousands):', min_value = 19.5, max_value = 350.0, value = 19.8)
            acs_TikTok_NI = st.slider('Percentage of Cummulative Followers each TikTok post makes an impression on that leads to atleast a single visit on Eikona material:', min_value = 1.0, max_value = 100.0, value = 50.0)

            impressions_perTikTokPost = (acs_TikTok *(float(acs_TikTok_NI)*0.01))

            st.header('Total # of Eikona impressions per TikTok post they make:' + str(impressions_perTikTokPost))

            tikTok_Posts = st.number_input('Number of Tiktok Posts Made:', min_value = 1, max_value = 10, value = 2)
            tikTok_redundancy_Loss = st.slider('Percentage of Redundancy Loss Per TikTok post (already seen/ignored)', min_value = 1.0, max_value = 100.0, value = 30.0, step = 0.5)

            TT_Posts = []

            for k in range(tikTok_Posts):
                TT_Posts.append(k)
            TT_Rates = []

            for m in TT_Posts:
                TT_Rates.append((impressions_perTikTokPost-(m*(tikTok_redundancy_Loss*0.01)))*1000)

            TT = {
                "Post": TT_Posts,
                "Impressions": TT_Rates
            }
            TT = pd.DataFrame(TT)
            st.write('TikTok Impressions for Eikona Per Posts made from ACS')
            st.write(TT)

            st.slider('Percentage of those TikTok conversions to Eikona_Site that download Lenz', min_value = 1.0, max_value = 100.0, value = 15.0)
            TT_Series = pd.Series(TT["Impressions"])

        with col2:

            st.header('Twitter')
            acs_Twitter = st.number_input('American Cancer Society Twitter Following(Millions):', min_value = 1.0, max_value = 2.0, value = 1.0, step = 0.1)
            acs_Twitter_NI = st.slider('Percentage of Cummulative Followers each Twitter post makes an impression on that leads to atleast a single on visit on Eikona material:', min_value = 1.0, max_value = 100.0, value = 50.0)

            impressions_perTwitterPost = (acs_Twitter *(float(acs_Twitter_NI)*0.01))

            st.header('Total # of Eikona impressions per Twitter post they make:' + str(impressions_perTwitterPost))

            twitter_Posts = st.number_input('Number of Twitter Posts Made:', min_value = 1, max_value = 10, value = 1)
            twitter_redundancy_Loss = st.slider('Percentage of Redundancy Loss Per Twitter post (already seen/ignored)', min_value = 1.0, max_value = 100.0, value = 30.0, step = 0.5)

            TW_Posts = []

            for j in range(twitter_Posts):
                TW_Posts.append(j)

            TW_Rates = []
            for d in TW_Posts:
                TW_Rates.append((impressions_perTwitterPost-(d*(twitter_redundancy_Loss*0.01)))*1000000)

            TW = {
                "Post": TW_Posts,
                "Impressions": TW_Rates
            }
            TW = pd.DataFrame(TW)
            st.write('Twitter Impressions for Eikona Per Posts made from ACS')
            st.write(TW)


            st.slider('Percentage of those Twitter conversions to Eikona_Site that download Lenz', min_value = 1.0, max_value = 100.0, value = 10.0)
            TW_Series = pd.Series(TW["Impressions"])


        ACS_TotalLenz = TT_Series.sum() + TW_Series.sum()

        st.header('-------------------------------------------------------------------------------------')
        st.header('-------------------------------------------------------------------------------------')
        st.header('-------------------------------------------------------------------------------------')

        st.header('Total People being reached with Lenz through ALL Current Marketing Strategies:')
        st.header(str(ACS_TotalLenz + total_reached_with_Lenz))
        




    #-------------------------
    ###Business Model Sidebar -- Lenz BMs
    #-------------------------
    if bm_sidebar == "Lenz Business Models":
        st.title('Lenz Business Models **** BROKEN*****')

        col1, col2 = st.columns(2)

        with col1:
            st.header('Lenz B2B Subscription')
            total_months = st.slider('Total Number of Months Being Looked at', min_value = 1, max_value = 48, value = 8, step = 1)
            total_months_per_business = []
            b2b_per_month = []
            total_b2b = []
            
            for i in range(total_months):
                b2b_per_month.append(avg_b2bsales)
                total_months_per_business.append(len(range(total_months)) - i)
                total_b2b.append(avg_b2bsales)
                total_b2b[i] += total_b2b[i]*i
            

            
            lenz_frame = {
                "Each Month" : b2b_per_month,
                "Months their subscription lasted" : total_months_per_business,
                "Total B2B Sales over period" : total_b2b
            }

            lenz_frame = pd.DataFrame(lenz_frame)
            st.write(lenz_frame)

            sub_price = st.number_input('Price per month to be integrated with Lenz', min_value = 10.0, max_value = 200.0, value = 50.0)
            sub_months = pd.Series(lenz_frame["Months their subscription lasted"]).sum()
            subscription_revenue = float(sub_months) * sub_price
            st.write('Total Revenue from Lenz B2B Subscriptions: ' + str(subscription_revenue))




    #-------------------------
    ###Business Model Sidebar -- Flywheel
    #-------------------------
    if bm_sidebar == "Flywheel":
        st.title('Flywheel Business Model')
    #-------------------------
    ###Business Model Sidebar -- AR Ads
    #-------------------------
    if bm_sidebar == "Ar Ads":
        st.title('AR Ads Business Model')




#st.subheader('Estimated Users in NFT Space')
if choose == "Other":
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


#st.subheader('Tokenomics')
if choose == "Tokenomics":
    st.header('Tokenomics')


    #initial values

    col1, col2 = st.columns(2)

    with col1:
        #initial values
        total_value = st.slider('Total Market Cap that starts in The Reserve: ', min_value = 100000, max_value = 5000000, value = 100000, step = 100000)
        total_coin = st.slider('Total Market Cap in The Reserve Token Count (Initial Circulating Supply)', min_value = 1000000000, max_value = 1000000000000, value = 1000000000, step = 1000000000)
        percent_coin_owned = total_coin
        #parameters
        people_involved = st.slider('Number of concurrent players a month: ', min_value = 10000, max_value = 100000000, value = 10000, step = 250)
        avg_min_month = st.slider('Average number of minutes walked in AR/Month: ', min_value = 1, max_value = 600, value = 30, step = 1)
        st.write('The Equivalent to: ' + str(float(avg_min_month/60)) + ' hours or ' + str(avg_min_month*60) + ' seconds')
        rate_per_sec_AR = st.slider('$EKO Generated each second in AR ad-compatible space: ', min_value = 0.001, max_value = 1.0, value = 0.01)
        x = (avg_min_month*60)*rate_per_sec_AR
        rate_of_generation = x #rate of $EKO per month being generated

        #days = 1000
        #total_coin = total_coin+people_involved*rate_of_generation*days
        #v1 is the value that our coin worth
        v1 = total_value*(percent_coin_owned/total_coin)
        #v2 is the value of a single coin
        v2 = v1/percent_coin_owned

        #d is the amount of days it takes for our coin to worth 1 dollar
        d = (total_value/1000*percent_coin_owned-percent_coin_owned)/(rate_of_generation*people_involved)


        fig = plt.figure()
        ax = plt.gca()


        v_ = []
        days_simulated = int(d)
        for i in range(days_simulated):
             total_coin = percent_coin_owned+people_involved*rate_of_generation*i
             v = total_value*(percent_coin_owned/total_coin)
             v_.append(v)

        ax.plot(range(days_simulated),v_)
        plt.xlabel("Number of months until $EKO is a people owned currency")
        plt.ylabel("The Reserve value over time")
        plt.xlim(1,60)


        fig.tight_layout()
        st.pyplot(fig)

        st.write('What this shows is the amount of coin we own over time vs. The ammount of concurrent players holdings(x) plotted against the number of months at those settings it will take before The Reserves initial market supply loses value to 1$')
    
    with col2:
        st.header('test')
