import json
import argparse
from pathlib import Path
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extraction.parser import parse_transcript

def generate_changelog(old_memo, new_memo, account_id):
    changes = []
    for key in old_memo:
        if old_memo[key] != new_memo.get(key):
            changes.append({
                "field_changed": key,
                "previous_value": old_memo[key],
                "new_value": new_memo.get(key),
                "reason": "Updated via onboarding transcript"
            })
            
    if not changes:
        return None
        
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "account_id": account_id,
        "changes": changes
    }
    
    log_dir = Path("changelog")
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / f"{account_id}_changelog.json"
    
    # Append if exists
    if log_path.exists():
        with open(log_path, 'r') as f:
            existing = json.load(f)
        existing.append(log_entry)
    else:
        existing = [log_entry]
        
    with open(log_path, 'w') as f:
        json.dump(existing, f, indent=2)
        
    return log_path

def update_pipeline(account_id, v1_memo_path, onboarding_transcript, v2_outdir):
    with open(v1_memo_path, 'r') as f:
        v1_memo = json.load(f)
        
    with open(onboarding_transcript, 'r') as f:
        text = f.read()
        
    updates = parse_transcript(text)
    
    v2_memo = v1_memo.copy()
    # Apply patches. Only update if the parser actually found something new.
    for k, v in updates.items():
        if k in v2_memo and v != "Unknown" and v != []:
            v2_memo[k] = v
            
    v2_memo["notes"] = "Updated from v2 onboarding call."
    # Clear resolved unknowns
    v2_memo["questions_or_unknowns"] = [q for q in v2_memo["questions_or_unknowns"] if "Missing" not in q]

    Path(v2_outdir).mkdir(parents=True, exist_ok=True)
    
    # Write V2 Memo
    memo_out = Path(v2_outdir) / f"{account_id}_memo.json"
    with open(memo_out, 'w') as f:
        json.dump(v2_memo, f, indent=2)
        
    # Changelog
    log_path = generate_changelog(v1_memo, v2_memo, account_id)
    if log_path:
        print(f"Changelog updated at {log_path}")
        
    return memo_out

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", required=True)
    parser.add_argument("--v1-memo", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--v2-outdir", required=True)
    args = parser.parse_args()
    
    update_pipeline(args.account, args.v1_memo, args.transcript, args.v2_outdir)