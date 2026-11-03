# Esau

**An evidence-driven, risk-aware BNB Chain investigation and trading agent.**

Esau watches BNB Chain, discovers contracts and token activity, investigates what it can verify, and remembers what it has already seen. Its long-term goal is to turn scattered on-chain evidence into a transparent, human-reviewed trading decision.

**No autonomous trading. No blind signals. Evidence first.**

## The problem

Tokens launch on BNB Chain faster than anyone can properly investigate them. A contract can look legitimate while hiding hostile behaviour. Liquidity can disappear, holders can be heavily concentrated, and the wallets behind a project may have a history worth examining.

The information needed to investigate these risks exists on-chain, but finding and connecting it takes time.

Esau is being built to do that investigation systematically, preserve the evidence, and make it easier for a person to decide what happens next.

## How it works

### What works today

1. **Watch the chain.** Connects to BNB Chain through JSON-RPC and monitors new blocks.
2. **Inspect activity.** Reads block transactions and identifies contract interactions and potential token activity.
3. **Investigate contracts.** Checks deployed bytecode and attempts to retrieve ERC-20 metadata such as name, symbol, decimals and total supply.
4. **Build memory.** Stores discovered tokens in a local SQLite database, so Esau can recognise tokens it has already encountered.
5. **Begin tracing origins.** Investigates deployment evidence and early interactions where the available RPC data allows it.

### What Esau is being built to do next

- **Reconstruct token history.** Connect deployments, factories, creators, first interactions and related wallet activity.
- **Screen contract behaviour.** Investigate honeypot patterns, suspicious permissions, taxes and other contract risks.
- **Analyse holders and liquidity.** Examine supply concentration, pool depth and trading activity.
- **Evaluate risk.** Combine verified evidence into an explainable risk assessment.
- **Prepare trade candidates.** Present qualifying opportunities with their supporting evidence for a person to approve or reject.

## What it does not do

Being clear about the boundaries matters when money is involved.

- **It does not execute trades.** There is currently no autonomous trading or unattended execution.
- **It does not claim to know everything about a token.** Some historical investigation requires archive-node access or better indexing than the current public RPC setup provides.
- **It remembers what it has seen.** Previously discovered tokens are stored locally rather than treated as new discoveries on every scan.
- **Its investigation is still developing.** Origin tracing is preliminary, and coordinated-wallet analysis, contract-risk detection and scoring are not yet complete.
- **A finding is not a verdict.** Esau is intended to distinguish verified facts, inferences and unknowns instead of presenting incomplete evidence as certainty.

## Stack

- **Language:** Python
- **Blockchain access:** Web3.py and BNB Chain JSON-RPC
- **RPC strategy:** Multiple public endpoints with connection checks and failover
- **Database:** SQLite via Python's built-in `sqlite3`
- **Application entry point:** `main.py`
- **Interface:** Command-line output; no web dashboard yet

## Running it locally

### Requirements

- Python 3.10 or newer
- Git
- Internet connection

### 1. Clone the repository

```bash
git clone https://github.com/AliFikan94/Esau.git
cd Esau
```

### 2. Create a virtual environment

**Windows (Git Bash):**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependency

```bash
python -m pip install --upgrade pip
python -m pip install web3
```

### 4. Start Esau

```bash
python main.py
```

Esau will attempt to connect to a configured BNB Chain RPC endpoint and begin monitoring new blocks.

**Configuration note:** The current development setup uses public RPC endpoints configured in `scanner/rpc.py`. No API keys or `.env` variables are required by the current setup. Public endpoints can be unreliable or rate-limited, and some do not provide historical state or transaction-receipt access.

The local SQLite database is stored as `esau.db` in the project directory and is excluded from Git.

## Status

**Actively developed · Pre-production · Not financial advice**

Esau is an early-stage project. Its scanner and persistent token memory are working; its deeper investigation and risk-analysis capabilities are still being built.

Built and maintained by one person.

## Author

**Fikan Ali**  
Full-stack developer based in Lagos, Nigeria.

fikanali94@gmail.com


Working across Python, Django, Flutter, JavaScript and Next.js.

[GitHub](https://github.com/AliFikan94)
