import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from io import BytesIO
from rembg import remove
import base64


top_image = Image.open('static/banner_top.png')
bottom_image = Image.open('static/banner_bottom.png')
main_image = Image.open('static/main_banner.png')

st.sidebar.image(top_image,use_column_width='auto')
format_type = st.sidebar.selectbox('Choose your AI magician 😉',["Text Processor","Image Captioner","Background Remover"])
st.sidebar.image(bottom_image,use_column_width='auto')
st.image(main_image,use_column_width='auto')
st.title("📄 Google's GenerativeAI Gemini+ 🏜 Streamlit")
left_co, cent_co,last_co = st.columns(3)
with cent_co:
      st.image('mits-logo.png', caption='Madhav Institute of Technology and Sciences,Gwalior')


if format_type == "Text Processor":
        st.title('Text Assisstant')
        API_KEY ="AIzaSyC4uKuTHWkFxFwpNkP6lmhsc1C7yQjreK8"
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
           error_msg = str(e)
           if "API_KEY_INVALID" in error_msg:
               st.error("Invalid API Key. Please enter a valid API Key.")
           else:
               st.error(f"Failed to configure API due to {error_msg}")    
    # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
    # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                 st.markdown(message["content"])

    # Accept user input
        if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
           st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
           with st.chat_message("user"):
              st.markdown(prompt)
   # Display assistant response in chat message container
        with st.chat_message("assistant"):
            chat = model.start_chat()
            if prompt is not None:
               response = chat.send_message(prompt, stream=True)
               for chunk in response:
                   st.write(chunk.text, end='')
               st.session_state.messages.append({"role": "assistant", "content": response})
               st.session_state.messages = []   
if format_type == "Background Remover":
    st.title("Background Remover")
    radio_input=st.radio(
        "Do you want to upload a image or capture a new one",
        [":rainbow[Upload]", "Capture:movie_camera:"],
        captions = ["Make Sure you have it in your machine", "Say Cheese"]
        )
    if radio_input==':rainbow[Upload]':
        my_upload = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if radio_input=='Capture:movie_camera:':
        my_upload = st.camera_input("Take a picture")
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    # Download the fixed image
    def convert_image(img):
       buf = BytesIO()
       img.save(buf, format="PNG")
       byte_im = buf.getvalue()
       return byte_im
    def fix_image(upload):
        image = Image.open(upload)
        col1.write("Original Image :camera:")
        col1.image(image)
        
        fixed = remove(image)
        col2.write("Fixed Image :wrench:")
        col2.image(fixed)
      

    col1, col2,col3 = st.columns(3)
    if my_upload is not None:
       if st.button('Upload'):
       
          fix_image(upload=my_upload)
    else:
       fix_image("./zebra.jpg")
       
if format_type == "Image Captioner":
    st.title("Image Captioner")
    radio_input=st.radio(
        "Do you want to upload a image or capture a new one",
        [":rainbow[Upload]", "Capture:movie_camera:"],
        captions = ["Make Sure you have it in your machine", "Say Cheese"]
        )
    if radio_input==':rainbow[Upload]':
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if radio_input=='Capture:movie_camera:':
        uploaded_file = st.camera_input("Take a picture")
    API_KEY ="AIzaSyC4uKuTHWkFxFwpNkP6lmhsc1C7yQjreK8"
    if uploaded_file is not None:
            if st.button('Upload'):
                if API_KEY.strip() == '':
                    st.error('Enter a valid API key')
                else:
                    file_path = os.path.join("temp", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    img = Image.open(file_path)
                    try:
                        genai.configure(api_key=API_KEY)
                        model = genai.GenerativeModel('gemini-pro-vision')
                        caption = model.generate_content(["Write a caption for the image in english",img])
                        tags=model.generate_content(["Generate 5 hash tags for the image in a line in english",img])
                        description=model.generate_content(["Describe the various details in the image",img])
                        st.image(img, caption=f"Caption: {caption.text}")
                        st.write(f"Tags: {tags.text}")
                        st.write(f"Description:{description.text}")
                    except Exception as e:
                        error_msg = str(e)
                        if "API_KEY_INVALID" in error_msg:
                            st.error("Invalid API Key. Please enter a valid API Key.")
                        else:
                            st.error(f"Failed to configure API due to {error_msg}")
        


footer="""
  <style>
        a:link, a:visited {
            color: blue;
            text-decoration: dotted; /* Remove underline */
        }

        a:hover, a:active {
            color: skyblue;
        }
        .footer .p{
            font-size:10px;
        }

        /* Footer */
        .footer {
            position:fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height:10%;
            font-size:15px;
            color: white; 
            text-align: center;
            padding: 10px 0; 
        }
        .footer p{
            font-size:20px;
        }

        .footer a:hover {
            color: white;
        }
    </style>

    <div class="footer">
        <p><a href="https://www.linkedin.com/in/dhruv-charne-908848213/?originalSubdomain=in" target="_blank">Dhruv Charne</a></p>
    </div>
"""
st.markdown(footer,unsafe_allow_html=True)
