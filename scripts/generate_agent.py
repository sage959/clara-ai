import json
import argparse
from pathlib import Path

def generate_system_prompt(memo):
    # Builds the prompt instructions based on the memo config
    company = memo.get('company_name', 'the company')
    
    prompt = f"You are the voice assistant for {company}.\n\n"
    prompt += "BUSINESS HOURS FLOW:\n"
    prompt += "- Greet the caller.\n- Ask the purpose of their call.\n- Collect their name and phone number.\n"
    prompt += f"- Determine if it's an emergency. Definition: {memo.get('emergency_definition')}.\n"
    prompt += "- Route or transfer the call accordingly.\n- If transfer fails, apologize and take a message (Fallback).\n"
    prompt += "- Ask if they need anything else.\n- Close the call professionally.\n\n"
    
    prompt += "AFTER HOURS FLOW:\n"
    prompt += "- Greet the caller and state the office is closed.\n- Ask the purpose of the call.\n"
    prompt += "- Confirm if it is an emergency.\n- Collect name, number, and address.\n"
    prompt += "- Attempt transfer to on-call staff.\n- If transfer fails, assure them of a follow-up.\n- Close the call.\n"
    
    return prompt

def create_agent_spec(memo_path, output_dir, version="v1"):
    with open(memo_path, 'r') as f:
        memo = json.load(f)

    spec = {
        "agent_name": f"{memo['company_name'].replace(' ', '')}_Agent",
        "voice_style": "Professional and empathetic",
        "system_prompt": generate_system_prompt(memo),
        "variables": ["caller_name", "phone_number", "is_emergency"],
        "transfer_protocol": memo.get("call_transfer_rules"),
        "fallback_protocol": "Take a message and email to dispatch.",
        "version": version
    }

    out_path = Path(output_dir) / f"agent_spec_{version}.json"
    with open(out_path, 'w') as f:
        json.dump(spec, f, indent=2)
        
    print(f"Created agent spec {version} at {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--memo", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--version", default="v1")
    args = parser.parse_args()
    
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    create_agent_spec(args.memo, args.outdir, args.version)