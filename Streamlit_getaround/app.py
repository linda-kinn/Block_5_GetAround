import streamlit as st
import pandas as pd
import plotly.express as px

## Cufflink is also a python library that connects plotly with pandas so that we can create charts 
# directly on data frames. It basically acts as a plugin.

### Config
st.set_page_config(
    page_title="Getaround",
    layout="wide"
)

###  Set a title and presentation
st.title("Getaround Dashboard Analysis")

st.markdown("""
    Hello, here you will see some graph analysis to help you to optimize your activity and reduce your rental car delay.
    * We gonna answer questions to set up a threshold and a scope.
    * Then we gonna optimize your rental car price.
""")

#################################################################################
#####                                                                       #####
#####                          INTRODUCTION                                 ##### 
#####                                                                       #####
#################################################################################
st.markdown(""" This this the database where we gonna work""")

DATA_URL = ('src/data_clean_dataframe.csv')
@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

data = load_data()
st.write(data.head(10))

st.markdown("""
    Here is the list of questions :
* Question 1 : How often are drivers late for the next check-in ?
* Question 2 : How does it impact the next driver ?
* Question 3 : How many problematic cases will it solve depending on the chosen threshold and scope ?
* Question 4 : How many rentals would be affected by the feature depending on the threshold and scope we choose ?
* Question 5 : Which share of our ouwner's revenue would potentially be affected by the feature ?

By those questions, we have to decide :
* Threshold : How long should the mininum delay be ?
* Scope : Should we enable the feature for all cars ?, only Connect cars ?

Select question in the sidebar to see analysis
""")

#################################################################################
#####                                                                       #####
#####                         CREATING OF SIDE BAR                          ##### 
#####                                                                       #####
#################################################################################

st.sidebar.header('Questions')
st.sidebar.text('Select question to see the analysis')
st.sidebar.selectbox('Select a question :', 
                        ['Question 1',
                        'Question 2',
                        'Question 3',
                        'Question 4',
                        'Question 5'])
if st.sidebar.selectbox == 'Question 1':
    st.text('Question 1 : How often are drivers late for the next check-in ?')

#################################################################################
#####                                                                       #####
#####                         CREATING DATA FOR ANALYSIS                    ##### 
#####                                                                       #####
#################################################################################

mask1 = data['previous_rental'] == "Yes"
data_F1 = data.loc[mask1,:]

mask2 = data_F1['is_delay'] == "Yes"
data_F2 = data_F1.loc[mask2,:]

mask3 = data_F2['state'] == 'canceled'
data_F3 = data_F2.loc[mask3,:]

mask4 = data_F2['state'] == "ended"
data_F4 = data_F2.loc[mask4,:]

mask5 = data['state'] == 'canceled'
data_F5 = data.loc[mask5,:]

mask6 = data_F1['state'] == 'canceled'
data_F6 = data_F1.loc[mask6,:]

mask7 = data['delay_types'].isin(['No_delay', 'Less than an hours','1h to 3h'])
data_F7 = data.loc[mask7,:]

#################################################################################
#####                                                                       #####
#####                               QUESTION 1                              ##### 
#####                                                                       #####
#################################################################################
st.header("QUESTION 1 : How often are drivers late for the next check-in ?")

######## GRAPH 1 ######### 

st.subheader("Graph 1 - Percent of 'delay' of previous rental car")
fig1 = px.histogram(data_F1, x='is_delay', histnorm='percent')
st.plotly_chart(fig1)

st.markdown("""
Graph A - Quick data analysis :
* As we can see, drivers are at 56 % late for the previous_rental against 44% are not late. 
* Let's dig a bit about late rental : 
""")

#################################################################################
#####                                                                       #####
#####                               QUESTION 2                              ##### 
#####                                                                       #####
#################################################################################

st.header("QUESTION 2 : How does it impact the next driver ?")
st.markdown("=> To know how does it impact the next driver we gonna analyze late return")

######## GRAPH 2 ######### 

st.subheader("Graph 2 - Percent of 'state' of late return of previous rental car")
fig2 = px.histogram(data_F2, x='state', histnorm='percent')
st.plotly_chart(fig2)

st.markdown("""Graph 2 - Quick data analysis :
* With surprise, we can see that when the driver are late, 78% keep their rental against 22 next driver canceled their rental.""")

######## GRAPH 3 ######### 

st.subheader("Graph 3 - Percent of 'delay types' of late return of previous rental car")
fig3 = px.histogram(data_F2, x='delay_types', histnorm='percent', category_orders={'delay types' :["No_delay",
                                                                                                    "Less than an hours",
                                                                                                    "1h to 3h", 
                                                                                                    "3h to 6h", 
                                                                                                    "6h to 12h",
                                                                                                    "12h to 24h",
                                                                                                    "Two day", 
                                                                                                    "More than 3 days"]})
st.plotly_chart(fig3)

st.markdown("""Graph 3 - Quick data analysis :
* We can see with the Graph 3 that mostly people are late until 3h late. It's represent 90% of rental, this is huge !""")

######## GRAPH 4 #########

st.subheader("Graph 4 - Percent of 'time delta' of late return of previous rental car")
fig4 = px.histogram(data_F2, x='time_delta', histnorm='percent', category_orders={'time_delta' :["No_time_delta",
                                                                 "Less than an hours",
                                                                 "1h to 3h", 
                                                                 "3h to 6h", 
                                                                 "6h to 12h",
                                                                 "12h to 24h",
                                                                 "Two day", 
                                                                 "More than 3 days"]})
st.plotly_chart(fig4)

st.markdown(""" Graph 4 - Quick data analysis :
* Here we see that most of the late rental have a large gap with the next driver time. 
* 31 % had 6h to 12h between the next driver, 16 % had 3h to 6h and 25 % from 1h to 3h. 
* We can notice as well that 14% had no delay between two rental car.""")

######## GRAPH 5 #########

st.subheader("Graph 5 - Percent of 'delay types' of late return of previous rental car")
fig5 = px.histogram(data_F3, x='delay_types', histnorm='percent', category_orders={'delay types' :["No_delay",
                                                                                                    "Less than an hours",
                                                                                                    "1h to 3h", 
                                                                                                    "3h to 6h", 
                                                                                                    "6h to 12h",
                                                                                                    "12h to 24h",
                                                                                                    "Two day", 
                                                                                                    "More than 3 days"]})
st.plotly_chart(fig5)

st.markdown("""Graph 5 - Quick data analysis :
* Just for checking, on the state 'canceled', there is no time delay because they cancelled their rental car""")


######## GRAPH 6 #########

st.subheader("Graph 6 - Percent of 'delay types' of late return of previous rental car")
fig6 = px.histogram(data_F3, x='time_delta', histnorm='percent', category_orders={'delay types' :["No_time_delta",
                                                                                                "Less than an hours",
                                                                                                "1h to 3h", 
                                                                                                "3h to 6h", 
                                                                                                "6h to 12h",
                                                                                                "12h to 24h",
                                                                                                "Two day", 
                                                                                                "More than 3 days"]})
st.plotly_chart(fig6)

st.markdown("""Graph 6 - Quick data analysis :
* Here we can analyze that mostly of the 'canceled' state, had a gap of 6h to 12h at 35% and 17% with a gap from 3h to 6h. 
* We can notice that this is not only because le previous rental are late. But they just canceled for unknow reason.
* But from no time delta to 3h late represent 42% of cancelation""")

######## GRAPH 7 #########

st.subheader("Graph 7 -Percent of 'checkin type' of late return of previous rental car")
fig7 = px.histogram(data_F3, x='checkin_type', histnorm='percent')
st.plotly_chart(fig7)

st.markdown("""Graph 7 - Quick data analysis :
* Just to check the checkin_type distribution and as they are almost 50/50, this is not a feature that affect delay. """)

######## GRAPH 8 #########

st.subheader("Graph 8 - Percent of 'delay types' of late return of previous rental car")
fig8 = px.histogram(data_F4, x='delay_types', histnorm='percent', category_orders={'delay_types' : ['No_delay', 
                                                                                                    'Less than an hours', 
                                                                                                    '1h to 3h', 
                                                                                                    '3h to 6h',
                                                                                                    '6h to 12h', 
                                                                                                    '12h to 24h', 
                                                                                                    'Two day']})

st.plotly_chart(fig8)

st.markdown("""Graph 8 - Quick data analysis :
* Most of people who keep their renting, can still rent the car until 3h late. it represent 87% under all delay_types""")

######## GRAPH 9 #########

st.subheader("Graph 9 - Percent of 'time_delta' of late return of previous rental car")
fig9 = px.histogram(data_F4, x='time_delta', histnorm='percent', category_orders={'delay_types' : ['No_time_delta',
                                                                                                    'Less than an hours',
                                                                                                    '1h to 3h', 
                                                                                                    '3h to 6h', 
                                                                                                    '6h to 12h', 
                                                                                                    '12h to 24h', 
                                                                                                    'two days']})

st.plotly_chart(fig9)

st.markdown("""Graph 9 - Quick data analysis :
* Initially, people keep their renting because the time_delta is longer than other. 
* We have 30% of people where the delta with previous rental last 6h to 12h. 
* Then from 1h to 3h is the delay we saw previously that next driver can 'accept' the late. 
* From 3h to 6h represent 16% that we can understand that is because the rate doest represent that more late (only 6%)""")

######## GRAPH 10 #########

st.subheader("Graph 10")
st.markdown("Percent of checkin_type of late return of previous rental car")
fig10 = px.histogram(data_F5, x='checkin_type', histnorm='percent')

st.plotly_chart(fig9)

st.markdown("""Graph 10 - Quick data analysis :
* From all cancelation the most chekin-in type is 'mobile' with 77%""")

#################################################################################
#####                                                                       #####
#####                               QUESTION 3                              ##### 
#####                                                                       #####
#################################################################################

st.header("QUESTION 3 : How many problematic cases will it solve depending on the chosen threshold and scope ?")

st.header("Setting the threshold and the scope ")

st.markdown("""From the analysis above :
* we can see that a threshold of 3h between rental car will solve 42 % of canceling. 
* But it is not only a minimum threshold we have to do because some canceling wasn't due to only delay. 
* We can state to a minimum canceling at 24h before and if it is less, canceler have to pay an adapt price as penalty. 
* In an other hand, check-in type has no influence about late, but there is 76% of canceling coming from Mobile check-in type. 

==> **Threshold** : 
 * Minimum time between two rental will be set up at 3h
 * Minimum canceling would be 24h before the time rental

 ==> **Scope** :
 * Even it is almost 50/50 with previous rental, the type of checking is up to 76% for mobile. We should have an action on it.""")

st.markdown("""#### >>> So, now, we gonna measure the impact of those features (Threshold and Scope)""")

#################################################################################
#####                                                                       #####
#####                               QUESTION 4                              ##### 
#####                                                                       #####
#################################################################################

st.header("QUESTION 4 : How many rentals would be affected by the feature depending on the threshold and scope we choose ?")

st.text("==> **Threshold** :") 
st.text(" Minimum time between two rental will be set up at 3h :")
st.text("=> It will solve : 86% late_rental (Graph 8)")
st.text("Minimum canceling would be 24h before the time rental")
st.text("=> It will solve : 100% of canceling (Graph 6)")

st.text("==> **Scope** :")
st.text("Even it is almost 50/50 with previous rental, the type of checking is up to 77% for mobile. ")
st.text("We should have an action on it. But need to know more about this feature.")

#################################################################################
#####                                                                       #####
#####                               QUESTION 5                              ##### 
#####                                                                       #####
#################################################################################

st.header("QUESTION 5 : Which share of our owner's revenue would potentially be affected by the feature ?")

st.text("1. The marketing")
st.text("2. App developpement with 'mobile' and 'connect'")
st.text("3. Legal")
st.text("4. Lawyer")











# st.balloons()