import streamlit as st 
st.title("Simple calculator")
a=st.number_input("enter the first number")
b=st.number_input("enter the second number")
c=st.selectbox("please select the operation",["Add","sub","mul","div"])
if st.button("calculator"):
    if c=="Add":
     st.write(f"Addition of a and b {a+b}")
     st.snow() 
    elif c=="sub":
      st.write(f"subraction of a and b {a-b}")
      st.snow()
    elif c=="mul":
      st.write(f"multiplication of a and b {a*b}")
      st.snow()
    elif c=="div":
     st.write(f"division of a and b {a/b}")
     st.snow()
    else:
        st.error("Cannot divide by zero")
      