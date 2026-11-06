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

Weeks 1-2: make the scanner trustworthy

Right now Esau starts from the moment it runs and remembers tokens it has seen. That's a toy scanner. The first job is turning it into a proper one.

Swap the SQLite table for something that can answer "what happened to this token between launch and now" without replaying the chain.
Add a backlog pass: when a new token appears, go back and pull its creation transaction and the first N trades, not just what happens after you noticed it.
Add retry and checkpointing so a dropped RPC call doesn't silently create a gap in the data. Log every gap you know about.
Provable by end of week 2: pick ten tokens that rugged in the last month, run Esau on them, and show it reconstructing their launch and first trades from scratch. That's a demo. You have nothing like it today.
Weeks 3-4: contract screening

This is the part with the clearest answer, so do it before anything statistical.

Honeypot detection: attempt a simulated buy and sell against the contract and see whether the sell reverts.
Ownership and permission flags: is ownership renounced, is there a mint function, can the owner pause transfers or change tax, is there a blacklist.
Tax detection: read buy and sell tax from the contract where it's readable, and flag the ones that are hidden or adjustable.
Provable by end of week 4: a table of twenty known scam tokens and twenty legitimate ones, with Esau's flags next to the truth. Publish the accuracy. Even if it's 70%, publishing it is the thing that makes people trust the rest.
Weeks 5-6: holders and liquidity

Holder distribution: top 10 and top 50 concentration, excluding known pool and burn addresses.
Liquidity: pool depth, whether LP tokens are locked and for how long, who holds them.
Wallet clustering: the same deployer, the same funding source, wallets funded within minutes of each other. This is where the scam signal actually lives.
Weeks 7-8: the score

Combine the above into one number with the reasoning attached, not a black box. Every point of the score should trace to a specific finding.
This is where you own the "evidence first" claim in your README. Most of these tools output a number and nothing else. Yours says "62, and here's why, and here's what I couldn't verify."
Provable by end of week 8: a working web page where someone pastes a contract address and gets a scored report. That's the moment Esau stops being a repo and becomes a product someone can use without a terminal.
Weeks 9-10: put it in front of ten real people

Ten people who trade BNB Chain memecoins. Not friends, not other devs. Give them the page, watch them use it, and write down where they got confused. Whatever they ignore, cut.

Weeks 11-12: the decision layer

Feed the score into a recommendation with the evidence attached, still requiring the human to approve.
Don't attempt autonomous execution. Everyone promises it and almost nobody has the safety story. Your restraint is a feature, and it's a better story at Demo Day than "it trades for you."

Built and maintained by one person.

## Author

**Fikan Ali**  
Full-stack developer based in Lagos, Nigeria.

fikanali94@gmail.com


Working across Python, Django, Flutter, JavaScript and Next.js.

[GitHub](https://github.com/AliFikan94)
