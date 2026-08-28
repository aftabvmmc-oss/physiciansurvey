import datetime
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Influenza Management Survey",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 3rem; }
        .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: 600; }
        .survey-header { background-color: #f0f4f8; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; }
    </style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# GOOGLE SHEETS CONNECTION PIPELINE
# ---------------------------------------------------------
@st.cache_resource
def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    # Fetch credentials from Streamlit secrets
    creds_dict = dict(st.secrets["gcp_service_account"])
    credentials = Credentials.from_service_account_info(
        creds_dict, scopes=scopes
    )
    return gspread.authorize(credentials)


def append_to_google_sheet(data_row: list):
    gc = get_gspread_client()
    sheet_id = st.secrets["sheets"]["spreadsheet_id"]
    worksheet_name = st.secrets["sheets"].get(
        "worksheet_name", 0
    )  # default first sheet

    sh = gc.open_by_key(sheet_id)
    ws = (
        sh.get_worksheet(0)
        if isinstance(worksheet_name, int)
        else sh.worksheet(worksheet_name)
    )
    ws.append_row(data_row, value_input_option="USER_ENTERED")


# ---------------------------------------------------------
# HEADER & STUDY INFORMATION
# ---------------------------------------------------------
st.markdown(
    """
<div class="survey-header">
    <h2 style="margin:0; color:#1e3d59;">Influenza Management Practices: Physician Questionnaire</h2>
    <p style="margin-top:8px; color:#435058; font-size:15px;">
        Assessment of diagnostic, therapeutic, and preventive strategies utilized by physicians in the management of Influenza.
    </p>
    <hr style="margin: 10px 0;">
    <small><b>Principal Investigator:</b> Dr. Aftab Ahmad (Contact: 9471391789 | aftab.ind@gmail.com)</small>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# FORM UI
# ---------------------------------------------------------

tabs = st.tabs(
    [
        "📋 1. Profile & Workload",
        "🔬 2. Diagnostics",
        "💊 3. Therapeutics",
        "💉 4. Vaccines",
        "🛡️ 5. Risk & Barriers",
        "📝 6. Recommendations",
    ]
)

# --- TAB 1: PROFILE & WORKLOAD ---
with tabs[0]:
    st.subheader("Physician Demographics & Clinical Workload")

    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input(
            "Email Address *", placeholder="doctor@example.com"
        )
        name = st.text_input("Name of Physician *", placeholder="Dr. John Doe")
        phone = st.text_input(
            "Phone Number (WhatsApp preferred) *",
            placeholder="10-digit mobile number",
        )
        specialty_opt = st.selectbox(
            "Specialty *",
            [
                "General Medicine",
                "Pulmonology/ TB Chest",
                "Obstetrics & Gynecology",
                "Pediatrics",
                "Geriatrics",
                "Other",
            ],
        )
        specialty = (
            st.text_input("Specify Specialty")
            if specialty_opt == "Other"
            else specialty_opt
        )

    with col2:
        qualification = st.selectbox(
            "Highest Qualification *",
            [
                "MBBS",
                "MD/MS",
                "DM/MCh or other super specialization",
                "PhD / Fellowship post MD/MS",
                "BDS/BAMS/BUMS/BHMS / BVMS",
                "Others",
            ],
        )
        designation = st.text_input(
            "Current Designation *",
            placeholder="e.g. Senior Resident, Consultant, Professor",
        )
        institution_opt = st.selectbox(
            "Institution *",
            [
                "All India Institute of Medical Sciences, New Delhi",
                "PSRI Hospital, New Delhi",
                "RIMS, Ranchi",
                "Sadar Hospital, Ranchi",
                "Alam Hospital, Ranchi",
                "Other Pvt Hospital, Ranchi",
                "Other",
            ],
        )
        institution = (
            st.text_input("Specify Institution")
            if institution_opt == "Other"
            else institution_opt
        )
        exp_years = st.selectbox(
            "Years in Clinical Practice (post-internship) *",
            [
                "Less than 5 years",
                "5-10 years",
                "11-20 years",
                "More than 20 years",
            ],
        )

    st.divider()
    st.markdown("#### Patient Volume & Baseline Knowledge")
    col3, col4 = st.columns(2)
    with col3:
        opd_per_week = st.number_input(
            "Approx. OPD patients seen per week *",
            min_value=0,
            max_value=5000,
            step=10,
        )
        ili_pct = st.slider(
            "Proportion of Influenza-Like Illness (ILI) among OPD patients (%) *",
            0,
            100,
            10,
            step=5,
        )
    with col4:
        ipd_per_week = st.number_input(
            "Approx. IPD/Emergency patients seen per week * (Enter 0 if not applicable)",
            min_value=0,
            max_value=2000,
            step=5,
        )
        sari_pct = st.slider(
            "Proportion of Severe Acute Respiratory Infection (SARI) among IPD (%) *",
            0,
            100,
            5,
            step=5,
        )

    st.divider()
    aware_guidelines = st.radio(
        "Are you aware of any guidelines for influenza management issued by any agency? *",
        ["Yes", "No"],
        horizontal=True,
    )
    guidelines_name = (
        st.text_input(
            "Mention the name of guideline(s) and issuing agency:"
        )
        if aware_guidelines == "Yes"
        else ""
    )

    training_received = st.radio(
        "Have you received any specific training in influenza management and vaccination guidelines? *",
        ["Yes", "No"],
        horizontal=True,
    )
    if training_received == "Yes":
        st.markdown(
            "##### Training Details",
            help="Details regarding past influenza training",
        )
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            t_agency = st.text_input("Name of training agency *")
            t_location = st.text_input("Location *")
        with t_col2:
            t_date = st.date_input(
                "When was training held? (Start date) *",
                value=datetime.date(2022, 1, 1),
            )
            t_duration = st.text_input(
                "Duration of training *", placeholder="e.g. 2 days, 1 week"
            )
    else:
        t_agency, t_location, t_date, t_duration = "", "", "", ""

# --- TAB 2: DIAGNOSTICS ---
with tabs[1]:
    st.subheader("Use of Diagnostics (RT-PCR & Lab Testing)")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        q2_1 = st.radio(
            "2.1. Primary reason for testing suspected acute fever/cough cases with RT-PCR *",
            [
                "To confirm bacterial co-infection",
                "To guide antiviral treatment decisions",
                "To detect influenza virus",
                "To determine ICU admission",
            ],
        )
        q2_2 = st.radio(
            "2.2. Recommended diagnostic test for laboratory confirmation *",
            [
                "Blood Culture",
                "Real Time Polymerase Chain Reaction (RT-PCR)",
                "Viral Inoculation",
                "Sputum Microscopy",
            ],
        )
        q2_3 = st.radio(
            "2.3. Estimated RTPCR Sensitivity *",
            ["50-79%", "80-89%", "90-99%", "100%"],
            horizontal=True,
        )

    with col_d2:
        q2_4 = st.selectbox(
            "2.4. Which ILI patient groups do you recommend RT-PCR testing? *",
            [
                "All patients with symptoms of ILI like cough and fever",
                "Patients with severe symptoms of ILI (high grade fever ≥102°F and severe sore throat)",
                "High risk groups (Age >65 years, with co-morbidities, obesity or pregnancy)",
                "Patients with symptoms and signs of complicated ILI (breathlessness, haemoptysis, seizure, worsening condition)",
            ],
        )
        q2_5 = st.selectbox(
            "2.5. Which SARI hospitalized patient groups do you recommend RT-PCR? *",
            [
                "All patients with symptoms of SARI like cough and fever requiring hospitalization",
                "Patients with severe symptoms only",
                "High risk groups (Age >65 years, with co-morbidities, obesity or pregnancy)",
                "Complicated patients (breathlessness, haemoptysis, altered sensorium, worsening conditions)",
            ],
        )
        q2_6 = st.multiselect(
            "2.6. In which patients is RT-PCR recommended as per MoHFW guidelines? (Select all that apply) *",
            [
                "Mild ILI cases in OPD",
                "SARI patients requiring hospitalization",
                "Patients with risk factors for severe disease",
                "Any patient with fever and cough",
            ],
        )

    st.divider()
    col_d3, col_d4 = st.columns(2)
    with col_d3:
        q2_7 = st.selectbox(
            "2.7. Is RT-PCR testing for influenza available at your institution? *",
            [
                "On-site available",
                "Available at affiliated lab (same city)",
                "Available at affiliated lab (different city)",
                "Not available",
            ],
        )
        q2_8 = st.selectbox(
            "2.8. Average Turnaround Time (TAT) for RT-PCR reports *",
            ["<24 hrs", "24-48 hrs", "48-72 hrs", ">3 days"],
        )
    with col_d4:
        q2_9 = st.select_slider(
            "2.9. % of OPD ILI patients undergoing RT-PCR testing *",
            options=[
                "<10%",
                "10-25%",
                "26-50%",
                "50-75%",
                "75-99%",
                "100%",
            ],
        )
        q2_10 = st.select_slider(
            "2.10. % of Ward SARI patients undergoing RT-PCR testing *",
            options=[
                "<10%",
                "10-25%",
                "26-50%",
                "50-75%",
                "75-99%",
                "100%",
            ],
        )
        q2_11 = st.select_slider(
            "2.11. % of ICU/HDU SARI patients undergoing RT-PCR testing *",
            options=[
                "<10%",
                "10-25%",
                "26-50%",
                "50-75%",
                "75-99%",
                "100%",
            ],
        )

# --- TAB 3: THERAPEUTICS ---
with tabs[2]:
    st.subheader("Use of Therapeutics (Antivirals & Protocols)")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        q3_1 = st.radio(
            "3.1. First-line antiviral recommended in high-risk patients *",
            ["Oseltamivir", "Azithromycin", "Dexamethasone", "Ceftriaxone"],
            horizontal=True,
        )
        q3_2 = st.radio(
            "3.2. When should antivirals ideally be started? *",
            [
                "Within 48 hours of symptom onset",
                "Only after laboratory confirmation",
                "After 5 days if symptoms persist",
                "Only in ICU-admitted patients",
            ],
        )
        q3_4 = st.radio(
            "3.4. Recommended duration of antiviral therapy for uncomplicated influenza *",
            ["3 days", "5 days", "7 days", "10 days"],
            horizontal=True,
        )

    with col_t2:
        q3_3 = st.multiselect(
            "3.3. Patient groups prioritized for antiviral therapy as per MoHFW guidelines *",
            [
                "Pregnant women",
                "Elderly (≥65 years)",
                "Patients with comorbidities",
                "Children without comorbidities",
            ],
        )
        q3_5 = st.selectbox(
            "3.5. Which patient group do you routinely prescribe antivirals (e.g. Oseltamivir)? *",
            [
                "All patients with symptoms of ILI like cough and fever",
                "Patients with severe symptoms of ILI (high grade fever ≥102°F and severe sore throat)",
                "High risk groups (Age >65 years, with co-morbidities, obesity or pregnancy)",
                "Patients with symptoms and signs of complicated ILI",
            ],
        )
        q3_7 = st.selectbox(
            "3.7. Is Oseltamivir available in your hospital? *",
            [
                "Yes, in hospital supply (free of cost for patients)",
                "Yes, in pharmacy (patients purchase)",
                "No",
                "Don't know",
            ],
        )

    col_t3, col_t4 = st.columns(2)
    with col_t3:
        q3_6 = st.multiselect(
            "3.6. Factors influencing your decision to prescribe antivirals *",
            [
                "Disease severity",
                "Patient comorbidities",
                "Patient presenting within 48-72 hrs of onset",
                "Laboratory confirmation",
                "Institutional guidelines",
                "Patient affordability",
            ],
        )
    with col_t4:
        q3_8 = st.multiselect(
            "3.8. Reasons for delayed antiviral initiation *",
            [
                "Late presentation (>48 hours)",
                "Awaiting confirmation / Drug not available",
                "Cost concerns",
                "Not needed clinically",
            ],
        )

    st.divider()
    st.markdown("##### Proportion of Confirmed Patients Receiving Antivirals")
    ct1, ct2, ct3 = st.columns(3)
    with ct1:
        q3_9 = st.selectbox(
            "3.9. OPD ILI Confirmed *",
            [
                "<10%",
                "10-25%",
                "26-50%",
                "50-75%",
                "75-99%",
                "100% (All)",
            ],
        )
    with ct2:
        q3_10 = st.selectbox(
            "3.10. Ward SARI Confirmed *",
            ["<10%", "10-25%", "26-50%", "50-75%", "75-99%", "100%"],
        )
    with ct3:
        q3_11 = st.selectbox(
            "3.11. ICU/HDU SARI Confirmed *",
            ["<10%", "10-25%", "26-50%", "50-75%", "75-99%", "100%"],
        )

# --- TAB 4: VACCINES ---
with tabs[3]:
    st.subheader("Use of Influenza Vaccines")

    q4_1 = st.multiselect(
        "4.1. Which high risk groups do you recommend for Influenza vaccine? (Select all that apply) *",
        [
            "Children (6 month - 8 years)",
            "Children (6 month - 8 years) with co-morbidities",
            "Pregnant females",
            "Elderly (> 65 years)",
            "Adults with COPD / Bronchial Asthma",
            "Diabetes",
            "Cancer / Immunocompromised patients",
            "Heart Disease / Kidney Disease / Liver Disease",
            "Health care workers",
        ],
    )

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        q4_2 = st.selectbox(
            "4.2. Estimated proportion of high-risk patients prescribed vaccine in past year *",
            [
                "<10% vaccinated",
                "10-25% vaccinated",
                "26-50% vaccinated",
                "51-75% vaccinated",
                "76-99% vaccinated",
                "100% vaccinated",
                "Don't Know",
            ],
        )
        q4_4 = st.selectbox(
            "4.4. How frequently should healthcare workers receive vaccination? *",
            [
                "Annually",
                "Every 6 months",
                "Every 2 years",
                "Only when exposed to influenza patients",
            ],
        )
        q4_6 = st.selectbox(
            "4.6. How frequently are influenza vaccine strain compositions updated globally? *",
            [
                "Twice every year (for each hemisphere)",
                "Once every year",
                "Once every 3 years",
                "Not sure",
            ],
        )

    with col_v2:
        q4_3 = st.multiselect(
            "4.3. Factors influencing recommendation *",
            [
                "Scientific evidence",
                "Institutional policy",
                "Perceived effectiveness",
                "Patient demand",
            ],
        )
        q4_5 = st.selectbox(
            "4.5. Recommended timing for influenza vaccination in India *",
            [
                "Before the start of peak influenza season",
                "Anytime during the year",
                "Only after exposure to an influenza case",
                "Only during pregnancy",
            ],
        )
        q4_7 = st.selectbox(
            "4.7. Formulation recommended for use in India *",
            [
                "Southern Hemisphere formulation",
                "Northern Hemisphere formulation",
                "Both formulations are equally recommended",
                "Not sure",
            ],
        )

# --- TAB 5: RISK & BARRIERS ---
with tabs[4]:
    st.subheader("Burden, Risk Perception & System Barriers")

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        q49 = st.multiselect(
            "5.1. Peak influenza season months in your city *",
            [
                "January-February",
                "March-April-May",
                "June-July-August",
                "September-October",
                "November-December",
                "No clear seasonal pattern",
                "Don't know",
            ],
        )
        q50 = st.multiselect(
            "5.2. Patient groups most frequently presenting with severe influenza *",
            [
                "Elderly (≥65 years)",
                "Children (≤5 years)",
                "Pregnant women",
                "Patients with chronic diseases",
                "Immunocompromised patients",
                "Healthcare workers",
            ],
        )
        q58 = st.selectbox(
            "6.5. Does your institution offer influenza vaccination to healthcare workers? *",
            ["Yes, free of cost", "Yes, paid", "No", "Don't Know"],
        )

    with col_b2:
        q51 = st.select_slider(
            "5.3. Personal susceptibility to acquiring influenza at workplace *",
            options=[
                "Not susceptible",
                "Slightly susceptible",
                "Moderately susceptible",
                "Highly susceptible",
                "Extremely susceptible",
            ],
        )
        q52 = st.select_slider(
            "5.4. Concern about transmitting influenza to patients/family *",
            options=[
                "Not concerned",
                "Slightly concerned",
                "Moderately concerned",
                "Very concerned",
                "Extremely concerned",
            ],
        )
        q53 = st.select_slider(
            "5.5. Adherence to national guidelines reduces morbidity/mortality *",
            options=[
                "Strongly disagree",
                "Disagree",
                "Neutral",
                "Agree",
                "Strongly agree",
            ],
        )

    st.divider()
    col_b3, col_b4 = st.columns(2)
    with col_b3:
        q54 = st.multiselect(
            "6.1. Main barriers to recommending influenza testing *",
            [
                "Lack of availability of RT-PCR testing",
                "Cost concerns",
                "Time delay in results",
                "Lack of patient willingness",
                "Lack of institutional policy",
            ],
        )
        q55 = st.multiselect(
            "6.2. Major barriers to following national management guidelines *",
            [
                "Lack of awareness about national guidelines",
                "Limited diagnostic resources",
                "Cost constraints",
                "Patient refusal",
                "Limited antiviral availability",
            ],
        )
    with col_b4:
        q56 = st.multiselect(
            "6.3. Factors that would improve adherence *",
            [
                "Institutional policies supporting guideline adherence",
                "Regular training and CME programs",
                "Increased diagnostic access",
                "Government vaccination mandates",
            ],
        )
        q57 = st.multiselect(
            "6.4. Primary barrier to vaccination uptake in India *",
            [
                "Lack of awareness among physicians and patients",
                "Cost of vaccination",
                "Lack of availability of vaccines",
                "Fear of adverse events",
            ],
        )

    q63 = st.radio(
        "Have you ever taken the Influenza vaccine? *",
        ["Yes, in past 1 year", "Yes, but more than a year ago", "No"],
        horizontal=True,
    )

# --- TAB 6: RECOMMENDATIONS & SUBMISSION ---
with tabs[5]:
    st.subheader("Recommendations & Insights")
    q59 = st.text_area(
        "Strategies to improve influenza diagnosis in India (Optional):",
        height=80,
    )
    q60 = st.text_area(
        "Strategies to improve influenza treatment in India (Optional):",
        height=80,
    )
    q61 = st.text_area(
        "Strategies to improve influenza vaccination in India (Optional):",
        height=80,
    )
    q62 = st.text_area(
        "Any additional comments / insights (Optional):", height=80
    )

    st.markdown(
        "> **Consent Confirmation:** By clicking Submit, you confirm your consent to participate in this study."
    )
    submitted = st.button("Submit Questionnaire", type="primary")

# ---------------------------------------------------------
# SUBMISSION PROCESSING & DATA APPEND
# ---------------------------------------------------------
if submitted:
    if not email or not name or not phone or not designation:
        st.error(
            "⚠️ Please fill in all required demographic fields (Email, Name, Phone, Designation) in Tab 1."
        )
    else:
        # Construct the exact row format mirroring Google Form CSV output
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [
            timestamp,  # Timestamp
            email,  # 1. Email
            name,  # 2. Name of physician
            phone,  # 3. Phone Number
            specialty,  # 4. Specialty
            qualification,  # 5. Highest Qualification
            designation,  # 6. Current Designation
            institution,  # 7. Institution
            exp_years,  # 8. Years in clinical practice
            opd_per_week,  # 9. Approx OPD patients/week
            ili_pct,  # 10. % ILI among OPD
            ipd_per_week,  # 11. Approx IPD patients/week
            sari_pct,  # 12. % SARI among IPD
            aware_guidelines,  # 13. Guideline awareness
            guidelines_name,  # 14. Guideline names
            training_received,  # 15. Training received
            t_agency,  # 16. Training agency
            t_location,  # 17. Training location
            str(t_date) if t_date else "",  # 18. Training start date
            t_duration,  # 19. Training duration
            q2_1,  # 20. Reason for testing
            q2_2,  # 21. Recommended test
            q2_3,  # 22. Sensitivity
            q2_4,  # 23. ILI RTPCR recommendation
            q2_5,  # 24. SARI RTPCR recommendation
            ", ".join(q2_6),  # 25. MoHFW RTPCR criteria
            q2_7,  # 26. RTPCR availability
            q2_8,  # 27. RTPCR TAT
            q2_9,  # 28. % ILI OPD tested
            q2_10,  # 29. % SARI IPD tested
            q2_11,  # 30. % SARI ICU tested
            q3_1,  # 31. First-line antiviral
            q3_2,  # 32. Antiviral timing
            ", ".join(q3_3),  # 33. Prioritized groups MoHFW
            q3_4,  # 34. Duration uncomplicated
            q3_5,  # 35. Routine prescription group
            ", ".join(q3_6),  # 36. Prescription factors
            q3_7,  # 37. Oseltamivir availability
            ", ".join(q3_8),  # 38. Reasons delayed antiviral
            q3_9,  # 39. % ILI OPD antiviral
            q3_10,  # 40. % SARI IPD antiviral
            q3_11,  # 41. % SARI ICU antiviral
            ", ".join(q4_1),  # 42. High risk groups vaccine
            q4_2,  # 43. % High risk vaccinated
            ", ".join(q4_3),  # 44. Vaccine recommendation factors
            q4_4,  # 45. Vaccine frequency HCW
            q4_5,  # 46. Timing India
            q4_6,  # 47. Strain update frequency
            q4_7,  # 48. Formulation India
            ", ".join(q49),  # 49. Peak season months
            ", ".join(q50),  # 50. Severe groups
            q51,  # 51. Personal susceptibility
            q52,  # 52. Transmission concern
            q53,  # 53. Adherence reduces morbidity
            ", ".join(q54),  # 54. Testing barriers
            ", ".join(q55),  # 55. Guideline adherence barriers
            ", ".join(q56),  # 56. Adherence facilitators
            ", ".join(q57),  # 57. Vaccination barriers
            q58,  # 58. Institution offers vaccine
            q59,  # 59. Strategy diagnosis
            q60,  # 60. Strategy treatment
            q61,  # 61. Strategy vaccination
            q62,  # 62. Additional comments
            q63,  # 63. Ever taken vaccine
        ]

        try:
            with st.spinner("Recording response in database..."):
                append_to_google_sheet(row)
            st.success("✅ Thank you! Your response has been recorded successfully.")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Failed to submit response. Error: {str(e)}")
