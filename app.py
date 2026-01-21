from PIL import Image
import google.generativeai as genai
import os 
import pypdf
import cv2 
import numpy as np
from image2text import extract_text_image
from word2text import doc_text_extract
from pdfextractor import text_extractor
import streamlit as st

# Lets configure Gemini key
gemini_key = os.getenv('Google_API_KEY1')
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite',generation_config={'temperature':0.9})


# Lets create the Siderbar


st.sidebar.title(':red[Upload Your Notes:]')
st.sidebar.subheader(':blue[Only Upload Images,PDFs and Docx]')
user_file = st.sidebar.file_uploader('Upload Here: ',type=['pdf','docx','png','jpg','jpeg','jfif'])


if user_file:
    st.sidebar.success('File Uploaded Successfully')
    text=''
    if user_file.type == 'application/pdf':
        user_text = text_extractor(user_file)
    elif user_file.type in ['image/png','image/jpg','image/jpeg','image/jfif']:
        user_text = extract_text_image(user_file) 
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = doc_text_extract(user_file)
    else:
        st.sidebar.error('Enter the Correct file type')



# Lets create Main Page

st.title(':orange[Minutes of Meeting Generator: ]') 
st.subheader(':violet[This Application creates Generalized minutes of meeting using notes.]')
st.write('''
Follow These Steps:-
1. Upload the Notes in PDF,DOCX or Image Format.
2. Click 'Generate to get MOM.
''')

r=''


if st.button('Generate'):
    with st.spinner('Please wait....'):
        prompt = f'''
           <Role> You are an Expert in Writing and Formatting minutes of meetings.
           <Goal> Create minutes of meetings from the notes that user has provided.
           <Context> The user has provided some rough notes as text. Here are the notes {user_text}
           <Format> The output must Follow the below format
           * Title: Assume Title of the meeting 
           * Agenda : Assume Agenda of the meeting
           * Attendees : Name of the attendees(If name of the attendess is not there keep it NA)
           * Date and Place: Date and the place of the meeting (If not Provided keep it Online)
           * Body : The Body Should Follow the Following Sequence of points
              * Mention Key Points Discussed
              * Mention Highlight any Decision that has beek taken
              * Mention Actionable Items
              * Mention Any Deadline If  Dicussed
              * Mention Next Meeting Date if Dicussed
              * Add 2-3 Line of summary
            <Instructions>
            * Use Bullet Points and highlight  the import keywords by making them bold.
            * Generate the output in docx format
            '''
        response = model.generate_content(prompt)
        st.write(response.text)
        r = response.text

        if st.download_button(label='DOWNLOAD',data=response.text,file_name='mom_generated.txt',mime='text/plain'):
            st.success(f'Your file is Downloaded------------> {r}')