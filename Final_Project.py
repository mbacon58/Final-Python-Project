'''
Name: Matt Bacon
CS230: Section 4
Data: NCAA Stadiums

Description:
This program creates 4 pages in streamlit. The first and default page is the introduction and project
overview. The other 3 pages are for my 3 questions being asked. The three are how many stadiums are in a specified state?;
what stadiums were built in a specific year?; and lastly what’s the largest capacity stadium in various US states?
Within each of these pages there will be a scatter map, pie chart, and bar chart. Some additions I made to my code that we
did not cover in class is the import time function that corresponds to the spinner function, and I used a
different bar chart than what we did in class.
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
#import time

stadiums = pd.read_csv("stadiums-geocoded.csv")

state_abbr_dict = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'D.C.': 'Washington D.C.'
}
#Obstacle I overcame
stadiums["state"] = stadiums["state"].replace(state_abbr_dict)

#Creating state list
s_list = stadiums["state"].tolist()
state_list = set(s_list)
new_state_list = sorted(state_list)

#Sidebar with navigation link
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Introduction/Project Overview", "Number of stadiums in a selected state", "When stadiums were built", "Largest capacity stadiums"])

#Introduction
if page == "Introduction/Project Overview":
    title = '<div style="text-align:center;"><p style="font-family:Times New Roman; color:Blue; font-size: 40px;">Python Final Project!</p></div>'
    st.markdown(title, unsafe_allow_html=True)
    header = '<div style="text-align:center;"><p style="font-family:Times New Roman; color:Blue; font-size: 40px;">NCAA Stadiums</p></div>'
    st.markdown(header, unsafe_allow_html=True)
    header1 = '<div style="text-align:center;"><p style="font-family:Daytona; color:Black; font-size: 30px;">Introduction/Project Overview</p></div>'
    st.markdown(header1, unsafe_allow_html=True)

    #with st.spinner('One moment...'):
     #   time.sleep(1)

    from PIL import Image
    input_image = Image.open("C:/Users/mbhoc/OneDrive - Bentley University/Documents/CS 230/stadium1.jpg")
    st.image(input_image, caption="Bryant-Denny Stadium, University of Alabama", width=550, use_column_width=True)

    st.write("For this final project I will be presenting data on various NCAA stadiums in "
             "the U.S. For this web page I created a sidebar on the left hand side of the page "
             "to select different pages. The default page is the introduction/project overview "
             "page and you have the option to select the page in which you would like to find specific "
             "data on. You have the option to see the number of stadiums in a selected state, to see "
             "how many stadiums were built in a specific year, and lastly the largest capacity "
             "stadium in selected states.")

#Second page
state_count = {word: s_list.count(word) for word in s_list}


if page == "Number of stadiums in a selected state":
    st.subheader("How many stadiums are in a specified state?")
    st.write("This page allows you to select a state in the US and "
             "will then give you the number of stadiums and the stadium names. "
             "Under that you will see a interactive scatter map showing you all of the locations "
             "of the stadiums in the US.")

    selected_state_box = st.selectbox("Please select a state:", new_state_list)
    #Getting number of stadiums in selected state
    if selected_state_box in state_count:
        count = state_count[selected_state_box]
    #Getting stadium names
    s_name = stadiums[stadiums["state"] == selected_state_box]
    stadium_l = s_name["stadium"].tolist()
    new_stadium_name = ", ".join(stadium_l)
    #Output
    st.write(f"There is/are {count} stadium(s) in {selected_state_box}.")
    st.write(f"The stadiums are: {new_stadium_name}")
    #Creating map
    stadium_map = stadiums[["stadium", "latitude", "longitude"]]
    stadium_map.rename(columns={"latitude": "lat", "longitude": "lon"}, inplace=True)
    st.title("Scatter Plot with NCAA Stadium Locations")

    view_state = pdk.ViewState(
        latitude=40,
        longitude=-95,
        zoom=3,
        pitch=0)

    #Create a map layer
    layer1 = pdk.Layer(type='ScatterplotLayer',
                       data=stadium_map,
                       get_position='[lon, lat]',
                       get_radius=7000,
                       get_color=[0, 0, 255],
                       pickable=True
                       )

    #Second map layer
    layer2 = pdk.Layer('ScatterplotLayer',
                       data=stadium_map,
                       get_position='[lon, lat]',
                       get_radius=2000,
                       get_color=[255, 0, 255],
                       pickable=True
                       )

    tool_tip = {"html": "Stadium Name:<br/> <b>{stadium}</b>",
                "style": {"backgroundColor": "red",
                          "color": "white"}
                }

    #Create a map
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=view_state,
        layers=[layer1, layer2],
        tooltip=tool_tip
    )

    st.pydeck_chart(map)

#Third page
if page == "When stadiums were built":
    st.subheader("What stadiums were built in between a certain time frame?")
    st.write("This page allows you to select a specific year "
             "by using a numeric slider. Once the year is selected "
             "you will receive the various stadiums built within the selected "
             "year. Under that you will see a pie chart that displays the "
             "percentage of the stadiums built in the specified year "
             "relative to all stadiums.")
    slider_num = st.slider("Please select a year", 1895, 2014)
    stadium_n = stadiums[stadiums["built"] == slider_num]
    stadium_built = stadium_n["stadium"].tolist()
    num_stadiums = len(stadium_built)
    total_stadiums = len(stadiums)

    if num_stadiums == 0:
        st.write(f"No stadium was built in {slider_num}")
    else:
        new_stadium_built = ", ".join(stadium_built)
        st.write(f"{num_stadiums} stadium(s) was/were built in {slider_num}: {new_stadium_built}")

    #Pie chart
    labels = [f"{num_stadiums} stadium(s) built", f"{total_stadiums} total stadiums"]
    sizes = [num_stadiums, total_stadiums]

    overall, built = plt.subplots()
    built.pie(sizes, labels=labels, autopct='%.1f%%')
    st.pyplot(overall)

#Fourth page
if page == "Largest capacity stadiums":
    st.subheader("What’s the largest capacity stadium in various US states?")
    st.write("This page allows you to select multiple states and in return "
             "portrays the largest capacity stadiums in those states. Below is a "
             "multiselect box where you can select your states. Under that is a bar "
             "chart that displays the states selected and their respected capacities. "
             "Under that it displays each state and stadium name with its capacity.")

    selected_state_multibox = st.multiselect("Please select a state:", new_state_list)
    state_stadiums = stadiums.loc[stadiums["state"].isin(selected_state_multibox)]
    if state_stadiums.empty:
        st.write(f"Please select a state.")
    else:
        max_capacity_stadiums = {}
        for state in selected_state_multibox:
            state_capacity = 0
            max_capacity_stadium = ""
            state_df = state_stadiums[state_stadiums["state"] == state]
            if not state_df.empty:
                for index, row in state_df.iterrows():
                    if row["capacity"] > state_capacity:
                        state_capacity = row["capacity"]
                        max_capacity_stadium = row["stadium"]
                max_capacity_stadiums[state] = (max_capacity_stadium, state_capacity)


        largest_capacity_stadiums = stadiums.loc[(stadiums["state"].isin(selected_state_multibox)) & (stadiums["stadium"].isin([s[0] for s in max_capacity_stadiums.values()]))]
        #Create a bar chart
        st.subheader("Selected State(s) Largest Capacity Stadium(s)")
        chart_data = largest_capacity_stadiums[["state", "capacity"]]
        chart_data = chart_data.set_index("state")
        st.bar_chart(chart_data)

        for state, (max_capacity_stadium, max_capacity) in max_capacity_stadiums.items():
            st.write(f"The largest capacity stadium in {state} is {max_capacity_stadium} with a capacity of {max_capacity:,}.")