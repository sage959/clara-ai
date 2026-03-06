import os
import glob
from pathlib import Path

# Importing the core functions directly to keep the batch script clean
from extract_info import create_memo
from generate_agent import create_agent_spec
from update_account import update_pipeline

def main():
    base_dir = Path(__file__).parent.parent
    demo_dir = base_dir / "data" / "demo_transcripts"
    onboarding_dir = base_dir / "data" / "onboarding_transcripts"
    out_dir = base_dir / "outputs" / "accounts"
    
    print("=== Starting Retell Pipeline A (Demo / v1) ===")
    demo_files = glob.glob(str(demo_dir / "*_demo.txt"))
    
    for demo_file in demo_files:
        filename = os.path.basename(demo_file)
        account_id = filename.split("_")[0]  # Extracts 'ACCT-100'
        
        account_out_v1 = out_dir / account_id / "v1"
        account_out_v1.mkdir(parents=True, exist_ok=True)
        
        # 1. Generate v1 Memo
        memo = create_memo(account_id, demo_file, account_out_v1)
        
        # 2. Generate v1 Agent Spec
        memo_path = account_out_v1 / f"{account_id}_memo.json"
        create_agent_spec(memo_path, account_out_v1, version="v1")
        
    print("\n=== Starting Retell Pipeline B (Onboarding / v2) ===")
    onboarding_files = glob.glob(str(onboarding_dir / "*_onboard.txt"))
    
    for onboard_file in onboarding_files:
        filename = os.path.basename(onboard_file)
        account_id = filename.split("_")[0]
        
        v1_memo_path = out_dir / account_id / "v1" / f"{account_id}_memo.json"
        account_out_v2 = out_dir / account_id / "v2"
        account_out_v2.mkdir(parents=True, exist_ok=True)
        
        if not v1_memo_path.exists():
            print(f"Skipping {account_id}: No v1 memo found.")
            continue
            
        # 1. Update Memo & Generate Changelog
        v2_memo_path = update_pipeline(account_id, v1_memo_path, onboard_file, account_out_v2)
        
        # 2. Generate v2 Agent Spec
        create_agent_spec(v2_memo_path, account_out_v2, version="v2")

    print("\n=== Pipeline Execution Complete ===")

if __name__ == "__main__":
    main()