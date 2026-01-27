import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the .env file locally
load_dotenv()

api_key = None

try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    # If st.secrets isn't set up (local dev), this catch prevents the crash
    api_key = os.getenv("GEMINI_API_KEY")


if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API Key not found!")


model = genai.GenerativeModel('gemini-1.5-flash')

def get_medicine_explanation(med_name):
    # 1. Clean the input (very important for dictionary/API lookups)
    query = med_name.strip().lower()
    
    # 2. Real-time API Call
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Explain what {query} is used for in two short, simple sentences for a patient. Do not include dosage."
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        print(f"API Error: {e}") # This shows up in your terminal

    # 3. Local Dictionary (The fallback) - Use lowercase keys for matching
    demo_meds = {
        "paracetamol": "Used to treat pain and reduce high temperature.",
        "amoxicillin": "An antibiotic used to treat bacterial infections.",
        "rolaids": "An antacid used to relieve heartburn and acid indigestion."
    }
    
    return demo_meds.get(query, f"The medication {med_name} is used as prescribed by your doctor for your specific symptoms.")
# --- SETUP (Mock Database) ---
if 'appointments' not in st.session_state:
    st.session_state.appointments = []

# --- SIDEBAR (Role Switcher) ---
role = st.sidebar.radio("Select User Role", ["Patient (Check-in)", "Doctor (Prescribe)", "Patient (View Prescription)"])

# --- FEATURE 1: SMART APPOINTMENT ---
if role == "Patient (Check-in)":
    st.header("📋 Patient Intake Form")
    
    # Use columns to organize the form like a real hospital document
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other", "Prefer not to say"])
        
    with col2:
        blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
        contact = st.text_input("Contact Number (Phone/Email)")

    st.divider() # Adds a visual horizontal line
    
    symptoms = st.text_area("Describe your symptoms / Reason for visit:")
    
    if st.button("Submit & Generate Token"):

        clean_name = name.strip()
        clean_contact = contact.strip()

        if not clean_name or not symptoms.strip() or not clean_contact:
            st.error("⚠️ Please fill in all required fields.")
        
        else:
            # 2. DUPLICATE CHECK
            # Using .get() prevents KeyError if old data exists
            is_duplicate = False
            for p in st.session_state.appointments:
                # We check name, contact, AND that they are still waiting
                if (p.get('name', '').lower().strip() == clean_name.lower() and 
                    p.get('contact', '').strip() == clean_contact and 
                    p.get('status') == "Waiting"):
                    is_duplicate = True
                    break # Found one, no need to keep looking

            if is_duplicate:
                st.warning(f"Hello {clean_name}, you already have an active token (# {p.get('id')}).")
                st.stop()
            # 4. IF WE REACHED HERE, IT IS NOT A DUPLICATE
            else:
                # Use a simple keyword match or API call for the Hackathon.
                department = "General Medicine" 
                symptoms_lower = symptoms.lower()
                if any(word in symptoms_lower for word in ["bone"]):
                    department = "Orthopedic"
                if any(word in symptoms_lower for word in ["oral", "teeth"]):
                    department = "Oral Health"
                if any(word in symptoms_lower for word in ["stomach", "constipation"]):
                    department = "Gastroenterologist"
                elif any(word in symptoms_lower for word in ["brain", "headache"]):
                    department = "Neurologist"
                token_id = len(st.session_state.appointments) + 1
                
                # Save to our "database"
                st.session_state.appointments.append({
                "id": token_id,
                "name": clean_name,
                "age": age,
                "gender": gender,
                "blood_type": blood_type,
                "contact": clean_contact,
                "symptoms": symptoms,
                "dept": department,
                "status": "Waiting",
                "prescription": None
            })
                
                st.success(f"Token Generated: #{token_id}")
                st.info(f"Please proceed to: {department}")

# --- FEATURE 2: DOCTOR PORTAL ---
elif role == "Doctor (Prescribe)":
    st.header("👨‍⚕️ Departmental Dashboard")

    # 1. Create Tabs for each Department
    # You can add more departments to this list as you expand
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "General", "Neurology", "Gastroenterology", "Cardiology", "Orthopedics"
    ])

    # Mapping internal names to Tab labels
    dept_mapping = {
        "General Medicine": tab1,
        "Neurologist": tab2,
        "Gastroenterologist": tab3,
        "Cardiology": tab4,
        "Orthopedics": tab5
    }

    # 2. Logic to display patients in the correct Tab
    for dept_name, tab_object in dept_mapping.items():
        with tab_object:
            st.subheader(f"{dept_name} Queue")
            
            # Filter the list for patients in THIS department who are WAITING
            dept_queue = [
                p for p in st.session_state.appointments 
                if p.get('dept') == dept_name and p.get('status') == "Waiting"
            ]

            if not dept_queue:
                st.write("No pending patients.")
            else:
                for patient in dept_queue:
                    # Create an "Expander" for each patient to keep the UI clean
                    with st.expander(f"Token #{patient['id']} - {patient['name']}"):
                        st.write(f"**Age:** {patient['age']} | **Blood Type:** {patient['blood_type']}")
                        st.write(f"**Symptoms:** {patient['symptoms']}")
                        
                        # Prescription Form inside the expander
                        medication = st.text_input(f"Prescribe for #{patient['id']}", key=f"med_{patient['id']}")
                        doctor_notes = st.text_area(f"Instructions", key=f"note_{patient['id']}")
                        
                        if st.button(f"Complete Appointment #{patient['id']}"):
                            if not medication:
                                st.error("Please prescribe medication before completing.")
                            else:
                                # 1. Trigger the AI Explainer
                                with st.spinner("AI is generating medicine notes..."):
                                    explanation = get_medicine_explanation(medication)
                                
                                # 2. Save everything to the record
                                patient['prescription'] = medication
                                patient['ai_explanation'] = explanation # NEW FIELD
                                patient['notes'] = doctor_notes
                                patient['status'] = "Completed"
                                
                                st.success("Prescription sent with AI explanation!")
                                st.rerun()

# --- FEATURE 3: PATIENT RESULTS ---
elif role == "Patient (View Prescription)":
    st.header("💊 Your Digital Prescription")
    token_input = st.number_input("Enter Token ID", min_value=1, step=1)
    
    if st.button("View My Record"):
        record = next((p for p in st.session_state.appointments if p['id'] == token_input), None)
        
        if record and record['status'] == "Completed":
            st.success(f"Prescription for {record['name']}")
            
            # Use standard headers to keep text sizes consistent
            st.markdown(f"### 💊 Medication: {record['prescription']}")
            
            st.markdown("---") # Visual separator
            
            st.markdown("#### 💡 What this medicine does:")
            st.info(record['ai_explanation']) 
            
            st.markdown("#### 👨‍⚕️ Doctor's Instructions:")
            st.write(record['notes'])
        else:
            st.warning("No completed record found for this Token.")