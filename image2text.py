import google.generativeai as genai
import cv2
import numpy as np
from PIL import Image
import os

def extract_text_image(image_path):
    file_bytes = np.asarray(bytearray(image_path.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    # lets Load and Process the image
    #image = cv2.imread(image) # Load the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # To convert BGR to RGB
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # To convert BGR to Grey
    _,image_bw = cv2.threshold(image_grey,150,255,cv2.THRESH_BINARY) # B&W conversion

    # The image that CV2 gives is in numpy array format, we need to convert it to image object
    final_image = Image.fromarray(image_bw) 

    # Configure genai Model
    key = os.getenv("Google_API_KEY1")
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    # Lets write prompt for OCR
    prompt = '''
        <role> You are an OCR (Optical Character Recognition) application.
        <Goal> Identify th characters in handwritten notes.
        <Context> user has provided an image of hanwritten notes
        <Instruction> 
        Do not generate any new content
        You can complete a word which is not Recognized
        make sure all the words are from englosh vocab or if thing or place why should make sense 
        Output should be well formated
        '''
    
    # Lets extrcat and return the text
    response = model.generate_content([prompt,final_image])
    output_text = response.text
    return output_text