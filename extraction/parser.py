import re

def parse_transcript(text):
    """
    Basic rule-based extractor. 
    TODO: Replace with local Ollama inference for better extraction accuracy.
    """
    data = {
        "company_name": _extract_field(text, r"Company:\s*(.*)"),
        "business_hours": _extract_field(text, r"Hours:\s*(.*)"),
        "services": _extract_list(text, r"Services:\s*(.*)"),
        "emergency_definitions": _extract_field(text, r"Emergency:\s*(.*)"),
        "routing_rules": _extract_field(text, r"Routing:\s*(.*)"),
        "integration_constraints": _extract_field(text, r"Integration:\s*(.*)"),
    }
    
    # Identify missing critical fields
    unknowns = []
    for k, v in data.items():
        if not v or v == "Unknown":
            unknowns.append(f"Missing information for {k}")
            
    data["questions_or_unknowns"] = unknowns
    return data

def _extract_field(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else "Unknown"

def _extract_list(text, pattern):
    val = _extract_field(text, pattern)
    return [s.strip() for s in val.split(',')] if val != "Unknown" else []