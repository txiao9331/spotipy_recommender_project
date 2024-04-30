import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image

if True:
    print('hello')

# ###### To run streamlit page type in terminal 
# ######## streamlit run file_name.py

####### Title + text
st.title('Welcome to Streamlit my first web page')
st.header('This is freakin coool!')

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")
    st.success("Done!")
# # #####  Data input - Birthday
# d = st.date_input('When is your BD?', datetime.date(2019,7,6), min_value=datetime.date(1900,1,1))
# st.write('Your BD is: ', d)

# # ######## Data input - Select a value
# x = st.slider('Select a value')
# st.write('The square value of ' + str(x) + ' is: ', x**2)

# # ####### Creating DF
# st.write(pd.DataFrame({'A': [1,2,3,4]}))

# # #### Select box
# select_box = st.selectbox('Happy it is Friday today?', ['Yes', 'No'])

# ### Creating checklists
# st.write('Here you can add your condition:')
# checkbox_one = st.checkbox("Yes")
# checkbox_two = st.checkbox("No")

# if checkbox_one and checkbox_two:
#     st.write('You selected both!')
# elif checkbox_one:
#     st.write('You selected only checkbox_one')
# elif checkbox_two:
#     st.write('You selected only checkbox_two')
# else:
#     st.write('You selected no checkboxes, boohoo')

# st.write(checkbox_one, checkbox_two)


# ########## CHARTS ################
# ##### Line Chart
# st.write('Line chart just here')
# chart_data = pd.DataFrame( np.random.randn(10, 2), columns=[f"Col{i+1}" for i in range(2)] )
# st.write(chart_data)
# st.line_chart(chart_data)

# ##### Bar chart
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=["a", "b", "c"])
# st.write(chart_data)
# st.bar_chart(chart_data)

# # ######## Map chart
# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [48.85, 2.38],
#     columns=['lat', 'lon'])
# st.write(df)
# st.map(df)

# # ######## Metrics bins ###########
# col1, col2, col3 = st.columns(3)
# col1.metric("Temperature", "70 °F", "1.2 °F")
# col2.metric("Wind", "9 mph", "-8%")
# col3.metric("Humidity", "86%", "4%")

# # ###### Side bar ###########
# selectbox = st.sidebar.selectbox( "Do you like Streamlit?", ["I'm totally in love", "Nope"],1) ## 1 is a unique key
# st.code(f"You selected {selectbox}")

# # ###### Video file ##########
# st.subheader('Some more music, our friday hymn!')
# st.video('https://www.youtube.com/watch?v=1TewCPi92ro&t=1s')

# # ### text input
# a_song_mayhaps = st.text_input(label='Enter a song!')
# st.write(a_song_mayhaps)

# ##### Image #########
# image = Image.open('mushu.png')
# st.image(image, caption='Happy weekend by Mushu') 

# st.balloons()


# st.audio(None, format='audio/mp3')
