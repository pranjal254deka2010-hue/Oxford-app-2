import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="OPI Portal", layout="centered")

# --- DATA STORAGE ---
if not os.path.exists("payments.csv"):
    pd.DataFrame(columns=["Date", "Name", "Purpose", "Amount"]).to_csv("payments.csv", index=False)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #002e63;'>OXFORD PARAMEDICAL INSTITUTE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>Dhupdhara, Goalpara, Assam | ESTD. 2009</p>", unsafe_allow_html=True)

st.divider()

menu = st.sidebar.selectbox("Menu", ["Create Receipt", "Payment History"])

if menu == "Create Receipt":
    st.subheader("📝 New Fees Receipt")
    with st.form("f1"):
        name = st.text_input("Student Name")
        course = st.selectbox("Course", ["DMLT", "ICU Technology", "ECG Tech", "First Aid"])
        purpose = st.selectbox("Purpose", ["Monthly Fee", "Admission Fee", "Registration Fee", "Other"])
        months = st.text_input("For Months (e.g. April to June)", "N/A")
        amt = st.number_input("Total Amount Paid (₹)", min_value=0.0)
        mode = st.selectbox("Mode", ["Cash", "Online", "UPI", "Cheque"])
        submit = st.form_submit_button("Generate Official PDF")

    if submit and name:
        today = datetime.now().strftime("%d-%m-%Y")
        # Save Record
        pd.DataFrame([[today, name, purpose, amt]], columns=["Date", "Name", "Purpose", "Amount"]).to_csv("payments.csv", mode='a', header=False, index=False)

        # Build PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.rect(5, 5, 200, 287) # Border
        
        if os.path.exists("logo.png"):
            pdf.image("logo.png", 10, 10, 30)
            
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "OXFORD PARAMEDICAL INSTITUTE", ln=True, align='C')
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 5, "Dhupdhara, Goalpara, Assam", ln=True, align='C')
        pdf.ln(20)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "OFFICIAL FEES RECEIPT", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Date: {today}", ln=True, align='R')
        pdf.cell(0, 12, f"Student: {name.upper()}", border='B', ln=True)
        pdf.cell(0, 12, f"Course: {course}", border='B', ln=True)
        pdf.cell(0, 12, f"Purpose: {purpose} ({months})", border='B', ln=True)
        pdf.cell(0, 12, f"Mode: {mode}", border='B', ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 15, f"TOTAL PAID: Rs. {amt}", border=1, ln=True, align='C')
        
        if os.path.exists("signature.png"):
            pdf.image("signature.png", 150, 160, 40)
            
        pdf.ln(40)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, "__________________________", ln=True, align='R')
        pdf.cell(0, 5, "Authorized Signatory      ", ln=True, align='R')

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.success("✅ Success! Your receipt is ready.")
        st.download_button("Download PDF", pdf_bytes, f"OPI_Receipt_{name}.pdf")

elif menu == "Payment History":
    st.subheader("💰 Collection Records")
    if os.path.exists("payments.csv"):
        st.dataframe(pd.read_csv("payments.csv"), use_container_width=True)
