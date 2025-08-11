# PII Detection & Masking Prototype 

This project is a lightweight PII detection and masking prototype for the WhoseDev AI IDE. It takes raw text input, detects sensitive entities like names, emails, developer secrets, phone numbers, and addresses, and replaces them with structured tokens.

---

## Tool Used

**spaCy** (`en_core_web_sm`) was chosen due to:

- Built-in Named Entity Recognition (NER)
- Fast performance and lightweight size
- Easy customization via `EntityRuler` for regex-based entities (API keys, emails, phone numbers, and addresses)

---

## Features

- Detects and masks:
  - `NAME` (full names)
  - `EMAIL` (email addresses)
  - `PHONE` (international/local phone numbers)
  - `ADDRESS` (basic street addresses like "42 Broad Street")
  - `API_KEY` (e.g. `sk_test_51XYZ...`)

- Outputs:
  - `masked_text` with `[LABEL:__TOKEN_N__]` tokens
  - `pii_map` with original values, labels, and confidence scores

---

## How to Run

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm

### Step 2: Run the script
```bash
python pii_masker.py

### Step 3: Output
The script will generate and print a structured JSON and save it as sample_output.json.

### Sample Input
```text
My name is Sarah Effiong and my email is effysarah3108@gmail.com, call me on +234 8065057728. I live at 42 Broad Street. Use API key sk_test_51XYZabcde to connect.

### Sample Output
See sample_output.json for the full JSON result.

### Files Included
pii_masker.py – main detection and masking script
sample_output.json – saved sample run output
README.md – this guide
requirements.txt – Python dependencies

### PII Labels Supported
NAME
EMAIL
PHONE
ADDRESS
API_KEY
