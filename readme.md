Retell Agent Automation Pipeline
This is a local, zero-cost pipeline I built to generate and update Retell voice agent configs based on call transcripts. It takes a raw demo call to spin up a base agent (v1), and then uses a subsequent onboarding call to patch the configuration (v2). It also generates a changelog during the update so we can track exactly what shifted between calls.

Architecture:
I split the logic into two main flows:

Pipeline A (v1 Setup): Demo Transcript -> extract_info.py (builds the Account Memo) -> generate_agent.py (generates the initial Agent Spec & Prompts)

Pipeline B (v2 Updates): Onboarding Transcript + v1 Memo -> update_account.py (creates v2 Memo + Changelog) -> generate_agent.py (generates the updated v2 Agent Spec)

Note on extraction: To keep this strictly zero-cost and local per the assignment constraints, the extraction layer currently uses a basic rule-based/regex parser.

Setup & Running:
Built with standard Python 3.9+. No external dependencies, heavy frameworks, or paid API keys required.

Drop your .txt transcripts into data/demo_transcripts/ and data/onboarding_transcripts/.

Run the orchestrator script from the root directory:
python scripts/batch_process.py

All generated JSON files will populate in outputs/accounts.

Limitations & Future Work
Extraction rigidity: The current parser relies on keyword markers in the transcript. In a real production environment, I'd swap the parser.py logic with an LLM call. To maintain the zero-cost constraint, hooking this up to a local Llama 3 model via Ollama would be the logical next step.

Changelog diffing: The state comparison in the update script handles flat dictionary changes well, but it's pretty basic. If the account schemas get more complex, it will need a more robust recursive diffing function to accurately track deep array changes.