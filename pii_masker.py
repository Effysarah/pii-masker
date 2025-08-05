import spacy
from spacy.pipeline import EntityRuler
import re
import json
import uuid

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# function to add custom rules
def add_custom_rules(nlp):
    if "entity_ruler" in nlp.pipe_names:
        nlp.remove_pipe("entity_ruler")

    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {
            "label": "API_KEY",
            "pattern": [{"TEXT": {"REGEX": r"sk_test_[a-zA-Z0-9]{10,}"}}]
        },
        {
            "label": "EMAIL",
            "pattern": [{"TEXT": {"REGEX": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"}}]
        },
        {
            "label": "PHONE",
            "pattern": [{"TEXT": {"REGEX": r"\+?\d[\d\s\-().]{7,}"}}]
        },
        {
            "label": "ADDRESS",
            "pattern": [
            {"TEXT": {"REGEX": r"\d{1,5}"}},
            {"TEXT": {"REGEX": r"[A-Z][a-zA-Z]+"}},
            {"TEXT": {"REGEX": r"(Street|St|Avenue|Ave|Road|Rd|Blvd|Lane|Ln)\.?"}}]
        }
    ]
    ruler.add_patterns(patterns)
    return nlp


nlp = add_custom_rules(nlp)

# function to Generate token name
def generate_token(label, index):
    return f"__TOKEN_{index}__"

# function to Detect PII entities using spaCy and regex
def detect_pii(text):
    doc = nlp(text)
    entities = []

    confidence_map = {
        "NAME": 0.95,
        "EMAIL": 0.99,
        "API_KEY": 0.97,
        "PHONE": 0.96,
        "ADDRESS": 0.93
    }

    for ent in doc.ents:
        if ent.label_ in ["PERSON", "EMAIL", "API_KEY", "PHONE", "ADDRESS"]:
            label = "NAME" if ent.label_ == "PERSON" else ent.label_
            confidence = confidence_map.get(label, 0.90)  # fallback if unknown
            entities.append({
                "start": ent.start_char,
                "end": ent.end_char,
                "label": label,
                "value": ent.text,
                "confidence": confidence
            })

    return entities

# function to Replace PII with tokens
def mask_text(text, entities):
    entities = sorted(entities, key=lambda x: x['start']) 
    masked_text = ""
    pii_map = {}
    cursor = 0

    for i, ent in enumerate(entities, start=1):
        token = generate_token(ent["label"], i)
        tag = f"[{ent['label']}:{token}]"
        masked_text += text[cursor:ent["start"]] + tag
        pii_map[token] = {
            "value": ent["value"],
            "label": ent["label"],
            "confidence": round(ent["confidence"], 2)
        }
        cursor = ent["end"]
    masked_text += text[cursor:]
    return masked_text, pii_map

# Main processing function
def process_text(text):
    entities = detect_pii(text)
    masked_text, pii_map = mask_text(text, entities)
    return {
        "masked_text": masked_text,
        "pii_map": pii_map
    }

# Test example
if __name__ == "__main__":
    sample_text = "My name is Sarah Effiong and my email is effysarah3108@gmail.com, call me on +234 8065057728. I live at 42 Broad Street. Use API key sk_test_51XYZabcde to connect."
    result = process_text(sample_text)
    print(json.dumps(result, indent=2))

with open("sample_output.json", "w") as f:
    json.dump(result, f, indent=2)
