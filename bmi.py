import streamlit as st
st.title("BMI Calculator")
height = st.radio("Select Your Height Format",['cms','meters','feet'])
weight = st.number_input("Enter your weight in kg")


if(height == 'cms'):
    height = st.number_input("Enter your height in cms")

    try:
        bmi = weight/(height/100)**2
    except:
        st.text("Enter Some Value of Height")

elif(height == 'meters'):
    height = st.number_input("Enter your height in meters")
    
    try:
        bmi = weight/(height)**2
    except:
        st.text("Enter Some Value of Height")

else:
    height = st.number_input("Enter your height in feet")
    try:
        bmi = weight/(height/3.28)**2
    except:
        st.text("Enter Some Value of Height")

if(st.button("Calculate BMI")):
    st.text("Your BMI Index is {}.".format(bmi))

    if(bmi<16):
        st.text("You are Severely Underweight.")

    elif(bmi>=16 and bmi<18.5):
        st.text("You are Underweight.")

    elif(bmi>=18.5 and bmi<25):
        st.text("You are Normal.")

    elif(bmi>=25 and bmi<30):
        st.text("You are Overweight.")

    else:
        st.text("You are Obese.")
        