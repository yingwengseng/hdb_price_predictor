import streamlit as st
import pandas as pd
import joblib

xgb = joblib.load('xgb.pkl')

st.title("HDB Price Predictor 🏠")

st.write("Welcome to the app! fill up the blanks to get your estimated hdb valuation")

floor_area_sqft = st.number_input("Enter floor_area_sqft:", min_value=0, max_value=2070)
commercial = st.number_input("if hdb has commercial unit, type 1 if yes, else 0:", min_value=0, max_value=1)
Mall_Within_2km = st.number_input("numbers of mall within 2km:", min_value=0, max_value=50)
Hawker_Within_2km = st.number_input("numbers of hawkers nearby within 2km (max 30):", min_value=0, max_value=30)
mrt_nearest_distance = st.number_input("mrt distance in meters:", min_value=0, max_value=1500)
mrt_interchange = st.number_input("if mrt station is an interchange, type 1, else 0:", min_value=0, max_value=1)
years_of_lease_left = st.number_input("how many years of lease left?:", min_value=0, max_value=95)
flat_type = st.selectbox("Select your flat type:", ["1 ROOM","2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"])
floor_level_range = st.selectbox("Select your floor level range:", ["Lower Level","Mid Lower Level", "Mid Upper Level", "Upper Level"])
closest_mrt_region = st.selectbox("Select the region the closest MRT belong to based on URA guidelines:", ["east", "north", "north_east", "west", "central"])
vacancy = st.number_input("estimate the vacancy in the primary school nearby:", min_value=0, max_value=120)

if flat_type == "1 ROOM":
    a, b,c,d,e = 0,0,0,0,0
elif flat_type == '2 ROOM':
    a, b,c,d,e = 1,0,0,0,0
elif flat_type == '3 ROOM':
    a, b,c,d,e = 0,1,0,0,0
elif flat_type == '4 ROOM':
    a, b,c,d,e = 0, 0,1,0,0
elif flat_type == '5 ROOM':
    a, b,c,d,e = 0, 0,0,1,0
else:
    a, b,c,d,e = 0, 0,0,0,1

if floor_level_range == 'Lower Level':
    f,g,h =0,0,0
elif floor_level_range == 'Mid Lower Level':
    f,g,h =1,0,0
elif floor_level_range == 'Mid Upper Level':
    f,g,h =0,1,0
else:
    f,g,h =0,0,1

if closest_mrt_region == 'east':
    i,j,k,l = 1,0,0,0
if closest_mrt_region == 'north':
    i,j,k,l = 0,1,0,0
if closest_mrt_region == 'north_east':
    i,j,k,l = 0,0,1,0
if closest_mrt_region == 'west':
    i,j,k,l = 0,0,0,1
else: 
    i,j,k,l = 0,0,0,0

# When user clicks the button
if st.button("Predict Price"):
 
    # Create a dataframe from inputs
    input_data = pd.DataFrame({
        'floor_area_sqft': [floor_area_sqft],
        'commercial': [commercial],
        'Mall_Within_2km': [Mall_Within_2km],
        'Hawker_Within_2km': [Hawker_Within_2km],
        'mrt_nearest_distance': [mrt_nearest_distance],
        'mrt_interchange': [mrt_interchange],
        'years_of_lease_left': [years_of_lease_left],
        '2 ROOM': [a],
        '3 ROOM': [b],
        '4 ROOM': [c],
        '5 ROOM': [d],
        'EXECUTIVE': [e],
        'Mid Lower Level': [f],
        'Mid Upper Level': [g],
        'Upper Level': [h],
        'east': [i],
        'north': [j],
        'north_east': [k],
        'west': [l],
        'vacancy': [vacancy],
        })   

    # ⚠️ Make sure preprocessing matches your training pipeline
    # (e.g., encoding, scaling, etc.)

    # Predict
    prediction = xgb.predict(input_data)[0]

    # Show result
    st.success(f"💰 Predicted HDB Price: ${prediction:,.0f}")