import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt # to add current date and time in that report,as we cannot get latest date from LLm

# comfigure the model

gemini_api_key=os.getenv('Gemini API Key2')
genai.configure(api_key=gemini_api_key)
model=genai.GenerativeModel('gemini-2.5-flash')

# Lets create SideBar for image upload.
st.sidebar.title(':orange[Upload the images of Defect Here:]')
uploaded_image=st.sidebar.file_uploader('Image',type=['jpeg','jpg','png','jfif'],accept_multiple_files=True)

uploaded_image=[Image.open(img) for img in uploaded_image]
if uploaded_image:
    st.sidebar.success('Images has  been uploaded Successfuly')
    st.sidebar.subheader(':blue[Uploaded Images]')
    st.sidebar.image(uploaded_image)

# Lets create the main page
st.title(':orange[Strutural Defect:-] : AI Assisted Structural Defect Identifier')    
st.markdown('#### :green[This application takes the images of structural defects from the construction site and prepares the AI assistant report]')
title=st.text_input('Enter the title of the report:')
name=st.text_input('Enter the name of the person who has prepared the report:')
desig=st.text_input('Enter the Designation of the person who has prepared the report:')
org=st.text_input('Enter the organisation of the person who has prepared the report:')

if st.button('Submit'):
    with st.spinner('Processing.......'):
        prompt=f'''
        <Role> You are an expert Structural Engineer with 20+ years of experience.
        <Goal> You need to prepare a detailed on the structural defect in the images provided by the user.
        <context> The Images shared by the user has been attached.
        <Format> Follow the steps to prepare the report
        * Add Title at the top of the report as the title provided by the user is {title}.
        * next add name ,designation and organization ,date of a person who has prepared the report.
        also include the date.
        name:{name}
        designation:{desig}
        organization:{org}
        date:{dt.datetime.now().date()}
        * Identify and classify the defects eg:- crack,
        * There could be more than one defects in images.Identify all defects seperately.
        * For each defect identified provide a short description of the defect and its potential impact on the structure.
        * For each defect measure the sevearity as low medium or high. also mentioning if the defect is inevitale or avoidable.
        * Provide the short term and long term solution for the repair along with an estimated cost in INR and Estimated time.
        * What precautionary measures can be taken to avoid these defects in future.
        
        <Instruction>
        * Do not include HTML format like <br> and anothers.
        * The report generated should be in word format.
        * Use Bullet points and tables whereever possible.
        * Make sure the report does not exceeds the 3 pages.'''

        response=model.generate_content([prompt,*uploaded_image],
                                        generation_config={'temperature':0.7})
        st.write(response.text)

    if st.download_button(
         label='Click to download',
         data=response.text,
        file_name='Structural_defect_report.txt',
        mime='text/plain'):
        st.success('Your File is Downloaded')