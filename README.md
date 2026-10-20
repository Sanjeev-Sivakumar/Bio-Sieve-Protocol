# The Bio-Sieve Protocol

> **A decentralized, air-gapped biosecurity verification platform engineered for high-throughput DNA synthesis facilities and secure biological foundries.**

[![Python Standard Library](https://img.shields.io/badge/Python-Standard_Library-102D4D?logo=python)](https://python.org)
[![Air-Gapped Compliance](https://img.shields.io/badge/Topology-100%25_Air--Gapped-168FA1)](https://github.com/Sanjeev-Sivakumar/Bio-Sieve-Protocol)
[![Zero Cloud Handshakes](https://img.shields.io/badge/Cloud_Exposure-ZERO-0EA5E9)](https://github.com/Sanjeev-Sivakumar/Bio-Sieve-Protocol)
[![Tests Passing](https://img.shields.io/badge/Tests-15%2F15_Passing-10B981)](https://github.com/Sanjeev-Sivakumar/Bio-Sieve-Protocol)

---

## 🔬 Architectural Overview

Modern gene synthesis operations face a critical deadlock: commercial synthesis screening typically relies on cloud-connected API endpoints, exposing proprietary intellectual property to remote servers and third-party infrastructure. 

**The Bio-Sieve Protocol** eliminates this vulnerability by executing 100% on-premise within isolated hardware boundaries. All incoming nucleotide sequences are screened against dual-use pathogen signatures, steganographic evasion patterns, and microchannel fluidic thresholds in real time without sending a single byte outside the local facility perimeter.

```
       SYNTHETIC NUCLEOTIDE INGESTION GATEWAY (FASTA)
                            │
               [Volatile Memory SHA-256 Digest]
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │               CORE BIO-SIEVE SCREENING ENGINE            │
 │                                                         │
 │  1. Aho–Corasick Multi-Pattern Automaton (O(N) Search)  │
 │  2. 3-Mer Frequency Vector Cosine Similarity Sieve      │
 │  3. Steganographic Fragment Affinity De-Shuffler        │
 │  4. Microchannel Thermal-Fluidic Physics Interlock      │
 │  5. Ephemeral Honey-Net Molecular Spooler (Decoy G-Code)│
 └─────────────────────────┬───────────────────────────────┘
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
 [PASS: ARMED // NOMINAL]         [THREAT FLAGGED: OVERRIDE]
 Dispense synthesis authorization  Active Honey-Net Hijack ->
 to physical synthesizer.          Inert Sucrose Lattice G-Code.
```

---

## ⚡ Core Subsystems & Capabilities

### 1. High-Speed Deterministic Exact Match Filtering
- **Automaton**: Linear-time Aho–Corasick finite-state string matching machine.
- **Reference Watchlist**: Identifies high-consequence pathogen signatures including Botulinum Neurotoxin, Ricin Ribosome-Inactivating Protein, Bacillus anthracis Lethal Factor, Restricted Orthopox Envelopes, and Dual-Use Cleavage Interlocks.
- **Complexity**: $O(N + M)$ traversal latency (executes in single-digit milliseconds).

### 2. Fuzzy Semantic Sequence Sieve
- **Algorithm**: Euclidean-normalized 3-mer frequency vector cosine similarity against calibrated restricted pathogen distributions.
- **Tripwire Threshold**: Calibrated at $\cos(\theta) \ge 0.8500$.
- **Detection Scope**: Flags obfuscated, mutated, or degenerate nucleotide homologies that evade deterministic exact matchers.

### 3. Steganographic Fragment Affinity De-Shuffler
- **Mechanism**: Multi-stride non-contiguous window scanner ($\text{strides} \in [1, 2, 3, 4, 5]$).
- **Complexity Metrics**: Shannon entropy ($H = -\sum p_i \log_2 p_i$), normalized alphabet entropy, and Lempel–Ziv compression ratio.
- **Affinity Matrix**: Computes dynamic token-bonding affinity matrices to detect and de-shuffle phased periodic threat fragments camouflaged inside benign carrier backbones.

### 4. Microchannel Thermal-Fluidic Physics Interlock
- **Physical Compiler Simulation**: Evaluates microsecond thermal, hydraulic, and kinetic conditions inside a physical synthesis nozzle ($L = 50\,\mu\text{m}$, $D_H = 12\,\mu\text{m}$).
- **Monitored Variables**: Flow velocity ($v$), Reynolds number ($\text{Re}$), thermal gradient ($\Delta T$), pressure drop ($\Delta P$), and kinetic rearrangement probability ($P_{\text{rearrange}}$).
- **Safety Relay**: Automatically trips if $\Delta T > 0.8500\,\text{K}/\mu\text{m}$ or $P_{\text{rearrange}} > 82.00\%$, locking physical actuation in volatile memory.

### 5. Ephemeral Honey-Net Invalidation Engine
- **Decoy Neutralization**: Upon safety envelope violation, the system transparently intercepts synthesis execution.
- **G-Code Redirection**: Replaces hazardous manufacturing parameters with safe, inert sucrose lattice printing coordinates (`inert_sugar_blueprint.gcode`).
- **Mesh Ledger**: Logs immutable isolation audit tokens in local peer registry memory.

### 6. Hardware Enclosure & Homomorphic Synchronization
- **Hardware Isolation**: Simulated hardware enclave perimeter with volatile memory boundaries and PCR attestation measurements.
- **Satellite Update Broadcast**: Ingests encrypted threat watchlist packages and merges deltas directly into the reference database index via simulated additive homomorphic encryption in ciphertext space without decrypting plaintexts.

---

## 📊 Presentation Deck & Documentation

The official competition slide deck and architectural blueprints are available directly in this repository:
- **Presentation Deck (PDF)**: [`Bio SIeve Protocol.pdf`](./Bio%20SIeve%20Protocol.pdf)
- **PowerPoint Deck (PPTX)**: [`Bio SIeve Protocol.pptx`](./Bio%20SIeve%20Protocol.pptx)
- **High-Resolution Slide Exports**: Located in the [`Bio SIeve Protocol/`](./Bio%20SIeve%20Protocol/) directory:
  - `Slide1.PNG` – Protocol Title & Air-Gapped Topology
  - `Slide2.PNG` – Decoupling Data Access from Biomedical Analysis
  - `Slide3.PNG` – Local Architecture & Standard Library Framework
  - `Slide4.PNG` – Runtime Physics Interlocks & Active Decoy Honey-Nets
  - `Slide5.PNG` – Innovation and Creativity
  - `Slide6.PNG` – Impact and Relevance
  - `Slide7.PNG` – Technical Quality & Validation Matrices
  - `Slide8.PNG` – System Execution Flowchart
- **Google Drive Presentation Folder**: [Google Drive Deck Access](https://drive.google.com/drive/folders/10k-tbMdE30vJ5d2VdZpnDgXNbewXMHdC?usp=sharing)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ (Standard Python installation; zero complex C++ or GPU prerequisites)

### Installation
Clone the repository and install the lightweight runtime dependencies:
```bash
git clone https://github.com/Sanjeev-Sivakumar/Bio-Sieve-Protocol.git
cd Bio-Sieve-Protocol
pip install -r requirements.txt
```

### Running the Web Platform
Launch the interactive NovaCell-inspired analytical interface:
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

### Running Automated Test Suite
Verify all 15 unit and pipeline integration tests:
```bash
pytest tests -v
```

---

## 📁 Repository Structure

```
Bio-Sieve-Protocol/
├── .streamlit/
│   └── config.toml                  # Streamlit theme & server configuration
├── assets/                          # Biotechnology UI imagery
│   ├── exact_match.jpg
│   ├── fuzzy_analysis.jpg
│   ├── hero_cell.jpg
│   ├── homomorphic_sync.jpg
│   └── secure_enclave.jpg
├── Bio SIeve Protocol/              # High-res presentation slide PNGs (Slides 1-8)
│   ├── Slide1.PNG
│   └── ...
├── tests/                           # Complete pytest automated validation suite
│   ├── test_fragment_affinity.py
│   ├── test_pipeline.py
│   ├── test_thermal_interlock.py
│   └── test_validation_engine.py
├── app.py                           # Full Streamlit application & interactive UI
├── engine.py                        # Core algorithmic screening engine
├── fragment_affinity.py             # Steganographic fragment de-shuffler & entropy
├── thermal_interlock.py             # Microchannel fluidics & thermal interlock simulator
├── validation_engine.py             # Ephemeral honey-net invalidator & decoy G-code
├── dashboard.py                     # Auxiliary analytical visualization dashboard
├── synthetic_biosecurity_specimen.fasta # Canonical threat verification specimen
├── sample_benign.fasta              # Human actin benign control sequence
├── sample_threat.fasta              # Synthetic reference threat sequence
├── inert_sugar_blueprint.gcode      # Generated inert sucrose lattice coordinates
├── Bio SIeve Protocol.pdf           # Official presentation deck (PDF)
├── Bio SIeve Protocol.pptx          # Official presentation deck (PPTX)
├── requirements.txt                 # Python dependencies
└── README.md                        # Documentation
```

---

## 🔒 Security & Privacy Notice
All sequence parsing, Aho–Corasick automaton searches, vector similarities, and physics simulations are executed strictly in volatile process memory. Raw sequence strings are never persisted to disk, maintaining air-gapped biosecurity compliance and zero exposure of intellectual property.
