# Influenza Management Practices - Physician Questionnaire

A Streamlit-based web application designed to collect survey responses from physicians regarding diagnostic, therapeutic, and preventive strategies in the management of Influenza. 

This application replaces a traditional Google Form with a more interactive, multi-tab user interface while maintaining a direct data pipeline to the original Google Sheet. Responses are appended in real-time using the Google Sheets API, preserving exact schema parity with historical dataset exports.

## Features
* **Optimized UI/UX:** 63-question survey broken down into 6 logical tabs to prevent fatigue.
* **Dynamic Logic:** Conditional fields that only appear based on prior answers.
* **Direct Integration:** Submissions are pushed directly to a connected Google Sheet via `gspread`.
* **Mobile-Responsive:** Built on Streamlit to adapt to both desktop and mobile viewports.

## Prerequisites
* Python 3.9+
* A Google Cloud Project with the **Google Sheets API** and **Google Drive API** enabled.
* A Google Service Account with a generated JSON key.
* An existing Google Sheet with the Service Account email added as an **Editor**.

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
   cd YOUR-REPO-NAME
