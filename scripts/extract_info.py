import json
import os
import argparse
from pathlib import Path
import sys

# Add parent dir to path to import extraction
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extraction.parser import parse_transcript

def create_memo(account_id, transcript_path, output_dir):
    with open(transcript_path, 'r') as f:
        text = f.read()

    parsed_data = parse_transcript(text)
    
    # Map to expected memo schema
    memo = {
        "account_id": account_id,
        "company_name": parsed_data.get("company_name"),
        "business_hours": parsed_data.get("business_hours"),
        "office_address": "Unknown", # often missing in demos
        "services_supported": parsed_data.get("services"),
        "emergency_definition": parsed_data.get("emergency_definitions"),
        "emergency_routing_rules": parsed_data.get("routing_rules"),
        "non_emergency_routing_rules": "Take a message",
        "call_transfer_rules": "Transfer to main line if requested",
        "integration_constraints": parsed_data.get("integration_constraints"),
        "after_hours_flow_summary": "Emergency check -> Collect details -> Transfer or Assure follow-up",
        "office_hours_flow_summary": "Greeting -> Determine purpose -> Route",
        "questions_or_unknowns": parsed_data.get("questions_or_unknowns"),
        "notes": "Generated from v1 demo call."
    }

    out_path = Path(output_dir) / f"{account_id}_memo.json"
    with open(out_path, 'w') as f:
        json.dump(memo, f, indent=2)
    
    print(f"Created memo for {account_id} at {out_path}")
    return memo

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    create_memo(args.account, args.transcript, args.outdir)