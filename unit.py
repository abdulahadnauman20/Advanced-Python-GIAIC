import streamlit as st
st.markdown("<h1 style='color: purple; text-align: center;'>BMI Calculator</h1>", unsafe_allow_html=True)
st.title("Unit Converter")
convertunit = st.radio("Select Your Unit",['length','temperature','weight'])
input=st.number_input("Enter your value")
st.markdown("---")
if(convertunit == 'length'):
    unit = st.radio("Select Your Unit",['cms','meters','feet','inch'])
    to=st.radio("Convert to Unit",['cms','meters','feet','inch'])

    conversion={
        'meters':1,
        'feet':3.28,
        'inch':39.37,
        'cms':100
    }
    result=input*conversion[unit]/conversion[to]
    st.write(f'{input} {unit} is {result} {to}')

elif(convertunit == 'temperature'):
    unit = st.radio("Select Your Unit",['celsius','fahrenheit','kelvin'])
    to=st.radio("Convert to Unit",['celsius','fahrenheit','kelvin'])
    if unit == 'celsius':
        if to == 'fahrenheit':
            result=input*1.8+32
            st.write(f'{input} {unit} is {result} {to}')
        elif to == 'kelvin':
            result=input+273.15
            st.write(f'{input} {unit} is {result} {to}')
    elif unit == 'fahrenheit':
        if to == 'celsius':
            result=(input-32)/1.8
            st.write(f'{input} {unit} is {result} {to}')
        elif to == 'kelvin':
            result=(input-32)/1.8+273.15
            st.write(f'{input} {unit} is {result} {to}')
    else:
        if to == 'celsius':
            result=input-273.15
            st.write(f'{input} {unit} is {result} {to}')
        elif to == 'fahrenheit':
            result=(input-273.15)*1.8+32

    

elif(convertunit == 'weight'):
    unit = st.radio("Select Your Unit",['grams','kilograms','pounds'])    
    to=st.radio("Convert to Unit",['grams','kilograms','pounds'])
    conversion={
        'kilograms':1,
        'pounds':2.205,
        'grams':1000
    }
    result=input*conversion[unit]/conversion[to]
    st.write(f'{input} {unit} is {result} {to}')