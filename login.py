import streamlit as st 
st.title("Student login")
username="user"
password="1234"
a=st.text_input("enter the username")
b=st.text_input("enter the password") 
if st.button("login"):
    if a==username and b==password:
        st.write("login sucessful")
        st.balloons()
    else:
        st.write("Invalid")
