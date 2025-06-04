import streamlit as st
import numpy as np

# Dummy classifier for demonstration
class DummyClassifier:
    def predict(self, X):
        # Simple logic for demonstration
        adults, minors_over_3, minors_under_3, stay_length, room_type = X[0]
        if adults > 2:
            return ['Family']
        elif room_type == 1:
            return ['Business']
        else:
            return ['Couple']

class GuestProfileClassifier:
    def __init__(self):
        self.room_types = {
            'Single': 0,
            'Double': 1,
            'Suite': 2,
            'Family': 3
        }
        self.clf = DummyClassifier()

    def classify(self, adults, minors_over_3, minors_under_3, stay_length, room_type_str):
        room_type = self.room_types[room_type_str]
        features = np.array([[adults, minors_over_3, minors_under_3, stay_length, room_type]])
        return self.clf.predict(features)[0]

    def streamlit_ui(self):
        st.title("Guest Profile Classifier")
        with st.popover("Input Guest Information"):
            adults = st.number_input("Number of adults", min_value=0, max_value=10, value=1)
            minors_over_3 = st.number_input("Number of minors (3+ years)", min_value=0, max_value=10, value=0)
            minors_under_3 = st.number_input("Number of minors (under 3 years)", min_value=0, max_value=10, value=0)
            stay_length = st.number_input("Length of stay (nights)", min_value=1, max_value=30, value=1)
            room_type_str = st.selectbox("Type of room", list(self.room_types.keys()))
            submit = st.button("Classify")
            if submit:
                profile = self.classify(adults, minors_over_3, minors_under_3, stay_length, room_type_str)
                st.success(f"Closest profile assignment: **{profile}**")