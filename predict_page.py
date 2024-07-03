import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
import pickle
import pandas as pd

model=pickle.load(open("xgBoost.pkl","rb"))
scaler=pickle.load(open("scaler.pkl","rb"))


def age_transform(age):
    if(age=="18-24"):
        age=1
    elif(age=="25-29"):
        age=2
    elif(age=="30-34"):
        age=3
    elif(age=="35-39"):
        age=4
    elif(age=="40-44"):
        age=5
    elif(age=="45-49"):
        age=6
    elif(age=="50-54"):
        age=7
    elif(age=="55-59"):
        age=8
    elif(age=="60-64"):
        age=9
    elif(age=="65-69"):
        age=10
    elif(age=="70-74"):
        age=11
    elif(age=="75-79"):
        age=12
    else:
        age=13
    return age

def education_transform(education):
    if(education=="Never attended school or only kindergarten"):
        education=1
    elif(education=="Grades 1 through 8 (Elementary)"):
        education=2
    elif(education=="Grades 9 through 11 (Some high school)"):
        education=3
    elif(education=="Grade 12 or GED (High school graduate)"):
        education=4
    elif(education=="College 1 year to 3 years (Some college or technical school)"):
        education=5
    else:
        education=6
    return education

def income_transform(income):
    if(income=="less than $10,000"):
        income=1
    elif(income=="$10,000 to less than $15,000"):
        income=2
    elif(income=="$15,000 to less than $20,000"):
        income=3
    elif(income=="$20,000 to less than $25,000"):
        income=4
    elif(income=="$25,000 to less than $35,000"):
        income=5
    elif(income=="$35,000 to less than $50,000"):
        income=6
    elif(income=="$50,000 to less than $75,000"):
        income=7
    else:
        income=8
    return income

def show_predict_page():
    st.title('Diabetes Predictor')
    st.write("""### Enter the following details to predict if you are diabetic""")
    
    yes_no = ["Yes", "No"]
    highBP=st.selectbox("Do you have high blood pressure?", yes_no)
    highChol=st.selectbox("Do you have high cholesterol?", yes_no)
    cholCheck=st.selectbox("Have you had a cholesterol check in the last 5 years?", yes_no)
    bmi=st.number_input("Enter your BMI", min_value=0.0, max_value=100.0, value=0.0)
    smoker=st.selectbox("HAve you smoked at least 100 cigarettes in your entire life?", yes_no)
    stroke=st.selectbox("Have you ever had a stroke?", yes_no)
    heartDisease=st.selectbox("Have you ever been diagnosed with heart disease?", yes_no)
    phyAct=st.selectbox("Have you engaged in any physical activity in the last 30 dyas?", yes_no)
    fruits=st.selectbox("Do you eat fruits 1 or more times per day?", yes_no)
    veggies=st.selectbox("Do you eat vegetables 1 or more times per day?", yes_no)
    drinker=st.selectbox("Are you a heavy drinker?", yes_no, help="Adult male >14 drinks/week, Adult feamle>7 drinks/week")
    genHealth=st.slider("Rate your general health(1: Excellent - 5: Bad)", 1, 5, 1,help="On a scale of 1-5: \n1 = excellent \n2 = very good \n3 = good \n4 = fair \n5 = poor")
    mentalHealth=st.number_input("In the past 30 days, how many days have you felt mentally unhealthy?", min_value=0, max_value=30, value=0)
    phyHealth=st.number_input("In the past 30 days, how many days have you felt physically unhealthy?", min_value=0, max_value=30, value=0)
    diffWalk=st.selectbox("Do you have serious difficulty walking or climbing stairs?", yes_no)
    gender=st.selectbox("Select your gender",["Male","Female"])
    age=st.selectbox("Select your age category ", ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 or more"])
    education=st.selectbox("Select your education level", ["Never attended school or only kindergarten","Grades 1 through 8 (Elementary)","Grades 9 through 11 (Some high school)","Grade 12 or GED (High school graduate)","College 1 year to 3 years (Some college or technical school)","College 4 years or more (College graduate)"])
    income=st.selectbox("Select your income level",["less than $10,000","$10,000 to less than $15,000","$15,000 to less than $20,000","$20,000 to less than $25,000","$25,000 to less than $35,000","$35,000 to less than $50,000","$50,000 to less than $75,000","$75,000 or more"])
    
    submit=st.button("Predict")
    if submit:
        if highBP=="Yes":
            highBP=1
        else:
            highBP=0
        if highChol=="Yes":
            highChol=1
        else:
            highChol=0
        if cholCheck=="Yes":
            cholCheck=1
        else:
            cholCheck=0
        if smoker=="Yes":
            smoker=1
        else:
            smoker=0
        if stroke=="Yes":
            stroke=1
        else:
            stroke=0
        if heartDisease=="Yes":
            heartDisease=1
        else:
            heartDisease=0
        if phyAct=="Yes":
            phyAct=1
        else:
            phyAct=0
        if fruits=="Yes":
            fruits=1
        else:
            fruits=0
        if veggies=="Yes":
            veggies=1
        else:
            veggies=0
        if drinker=="Yes":
            drinker=1
        else:
            drinker=0
        if diffWalk=="Yes":
            diffWalk=1
        else:
            diffWalk=0
        if gender=="Male":
            gender=1
        else:
            gender=0
        age=age_transform(age)
        income=income_transform(income)
        education=education_transform(education)
        input_data=np.array([[highBP,highChol,cholCheck,bmi,smoker,stroke,heartDisease,phyAct,fruits,veggies,drinker,genHealth,mentalHealth,phyHealth,diffWalk,gender,age,education,income]])
        input_df=pd.DataFrame(input_data,columns=["HighBP","HighChol","CholCheck","BMI","Smoker","Stroke","HeartDiseaseorAttack","PhysActivity","Fruits","Veggies","HvyAlcoholConsump","GenHlth","MentHlth","PhysHlth","DiffWalk","Sex","Age","Education","Income"])
        input_data_scaled=scaler.transform(input_df)
        prediction=model.predict(input_data_scaled)
        st.write(input_data_scaled)
        st.write("Prediction: ",prediction[0])
        if prediction[0]==1:
            st.subheader("You are at risk of diabetes")
        else:
            st.subheader("You are not at risk of diabetes")