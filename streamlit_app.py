import streamlit as st
from PIL import Image
import requests

# URL = "https://imageapi-646220559180.europe-west1.run.app"
URL = "http://localhost:8000"
if st.button("![cliccami](https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png)"):
    st.write("Why you clicked me??")


img_file_buffer = st.file_uploader('Upload an image')

if img_file_buffer is not None:

  col1, col2 = st.columns(2)

  with col1:
    ### Display the image user uploaded
    st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")

  with col2:
    with st.spinner("Wait for it..."):
      ### Get bytes from the file buffer
      img_bytes = img_file_buffer.getvalue()

      ### Make request to  API (stream=True to stream response as bytes)
      res = requests.post(URL + "/upload_image", files={'file': img_bytes})

      if res.status_code == 200:
        ### Display the image returned by the API
        st.write(res.json())
      else:
        st.markdown("**Oops**, something went wrong 😓 Please try again.")
        print(res.status_code, res.content)
