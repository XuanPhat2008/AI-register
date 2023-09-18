import streamlit as st
import pandas as pd
import csv
import numpy
from PIL import Image

file_db = "user_db.csv"

import cv2

def lines():
    with open(file_db, 'r', encoding='utf8') as f:
        x = len(f.readlines())
        return x

def read_csv(username):
    with open(file_db, 'r', encoding='utf8') as f:
        for i in range(0, len(file_db)):
            user = f.readline().replace('\n', '').split(',')[0]
            if user == username:
                return True
        return False
        
def img_name(username):
    with open(file_db, 'r', encoding='utf8') as f:
        next(f)
        x = lines() - 1
        for i in range(0, x):
            info = f.readline().replace('\n', '').split(',')
            if username == info[0]:
                return info[1]

def write_csv(all_info):
    with open(file_db, 'a', newline='\n', encoding="utf8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(all_info)

def sign_up():
    st.title("Sign Up")
    new_username = st.text_input("Username")
    
    uploaded_image = st.file_uploader("Upload your selfie image", type=["jpg", "jpeg", "png"])

    # Check if an image was uploaded
    if uploaded_image is not None:
        # Display the uploaded image
        st.image(uploaded_image, caption="Upload success!", use_column_width=True)

    else:
        st.info("Please upload your selfie image.")
    
    if st.button("Sign Up"):
        if new_username:
            if read_csv(new_username):
                st.warning("Username already exists. Please choose another.")
            else:
                img = str(uploaded_image.type).replace('image/', '.')
                with open(new_username + img, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                a = [new_username, new_username+img]
                write_csv(a)
                st.success("Sign-up successful! You can now sign in.")

def sign_in():
    st.title("Sign In")
    username = st.text_input("Username")

    uploaded_image = st.file_uploader("Upload your selfie image", type=["jpg", "jpeg", "png"])

    # Check if an image was uploaded
    if uploaded_image is not None:
        # Display the uploaded image
        st.image(uploaded_image, caption="Upload success!", use_column_width=True)

    if st.button("Sign In"):
        img = str(uploaded_image.type).replace('image/', '.')

        with open("temp"+img, "wb") as f:
            f.write(uploaded_image.getbuffer())

        image1 = cv2.imread("temp"+img)
        image2 = cv2.imread(img_name(username))

        # Resize the uploaded image to match the dimensions of the stored image
        image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        diff_image = cv2.absdiff(gray_image1, gray_image2)

        percentage_diff = (numpy.count_nonzero(diff_image) / diff_image.size) * 100

        if read_csv(username) and percentage_diff == 0:
            st.success("Sign-in successful!")
            st.write(f"Welcome {username}")
            img = Image.open(img_name(username))
            st.image(img, caption="Upload success!", use_column_width=True)
        else:
            st.write(f"PATH: {img}, {img_name(username)}")
            st.write(f"Percentage: {percentage_diff}%")
            st.error("Authentication failed. Please check your credentials.")


# Main Streamlit app
def main():
    st.sidebar.title("User Authentication")
    choice = st.sidebar.radio("Choose an option", ["Sign Up", "Sign In"])

    if choice == "Sign Up":
        sign_up()
    elif choice == "Sign In":
        sign_in()

if __name__ == "__main__":
    main()
