# Phissss — Hybrid Phishing Defense System

Research project combining AI-based URL classification with blockchain-backed threat intelligence to detect and mitigate phishing attacks. Includes a full academic paper (LaTeX) and a working backend implementation.

## What It Does

- **AI Engine**: Classifies URLs as phishing/legitimate using ML models trained on URL features, DOM structure, and metadata
- **Blockchain Layer**: Logs confirmed phishing URLs to an immutable distributed ledger — prevents tampering and enables cross-org threat sharing
- **Backend API**: Python Flask server that accepts URL queries and returns risk scores
- **Research Paper**: Full LaTeX writeup covering methodology, architecture, and evaluation results

## Tech Stack

| Layer | Tech |
|-------|------|
| AI / ML | Python, scikit-learn / custom models |
| Blockchain | Ethereum / Web3 (smart contracts) |
| Backend | Python (Flask) |
| Document | LaTeX |
| Directories | `ai-hybrid/`, `ai_engine/`, `backend/`, `blockchain/` |

## Practical Use

Enterprise or institutional phishing defense — the hybrid approach addresses the weakness of pure-AI systems (adversarial evasion) by anchoring confirmed threat data on-chain, making the blocklist tamper-proof and shareable across organizations without a central authority.

## Structure

```
Phissss/
├── Hybrid-Phishing-Defense/
│   ├── ai-hybrid/       # Combined AI detection pipeline
│   ├── ai_engine/       # Core ML models
│   ├── backend/         # Flask API
│   └── blockchain/      # Smart contract + Web3 integration
├── Latex/               # Research paper source
│   └── Main.tex
└── MIni/                # Prototype / minimal demo
```
