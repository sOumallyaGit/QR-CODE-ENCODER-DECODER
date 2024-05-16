import qrcode
import cv2
import streamlit as st
import numpy as np
from io import BytesIO

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_array = BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()
    
    return img_byte_array

def decode_qr_code(image):
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)
    
    return data if data else None

st.title("QR Code Encoder and Decoder")

option = st.radio("Choose an option:", ("Generate QR Code", "Decode QR Code"))

if option == "Generate QR Code":
    data = st.text_input("Enter data to encode in QR code:")
    if st.button("Generate"):
        if data:
            try:
                qr_img = generate_qr_code(data)
                st.image(qr_img, caption="Generated QR Code", use_column_width=True)
            except Exception as e:
                st.error(f"Error generating QR code: {e}")
        else:
            st.error("Please enter data to encode.")
elif option == "Decode QR Code":
    uploaded_file = st.file_uploader("Upload a QR code image:", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        try:
            image_bytes = uploaded_file.getvalue()
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            decoded_data = decode_qr_code(image)
            if decoded_data:
                st.success(f"Decoded Data: {decoded_data}")
            else:
                st.error("No QR code found in the image.")
        except Exception as e:
            st.error(f"Error decoding QR code: {e}")
