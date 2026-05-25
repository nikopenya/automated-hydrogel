# Automated Soft-Matter Synthesis & Characterization Lab (ASMI-Opentrons Pipeline)

This repository contains the complete ecosystem of Python scripts and automation protocols developed for a high-throughput, data-driven hydrogel discovery platform. The pipeline integrates **Design of Experiments (DoE)** via Latin Hypercube Sampling (LHS), automated liquid handling formulation using an **Opentrons Flex**, and high-throughput mechanical characterization via a modified **Automated Soft Matter Indenter (ASMI)**.

---

## Repository Structure

The code is organized into three core operational phases:

### 1. Experimental Design (DoE via LHS)
Algorithms used to map multi-component composition spaces, maximizing formulation diversity while embedding rheological safety thresholds to avoid automated pipetting jams.
* `LHSlap.py`: Generates the 2D sampling space for the baseline **PEGDA/LAP** hydrogel system.
* `LHSpva.ipynb`: Interactive Jupyter Notebook executing the 3D sampling space for viscoelastically-toughened **PVA/PEGDA/LAP** semi-IPNs. Includes interactive Plotly visualizations.
* `LHSriboflavin.py`: Generates the 3D sampling matrix for biocompatible Type II **PEGDA/TEA/Riboflavin** photopolymerizable systems.

### 2. Automated Robotic Synthesis (Opentrons Flex Protocols)
API v2.21 scripts that command the Opentrons Flex robot to accurately dispense and mix stock solutions into standard 96-well SBS microplates.
* `LAPoptimo_1.py`, `LAPoptimo_2.py`, `LAPoptimo_3.py`: Batch synthesis protocols for the PEGDA/LAP system split into 3 consecutive microplates (32 unique formulations with 3 replicates each).
* `PVAoptimo_1.py`, `PVAoptimo_2.py`: Optimized high-viscosity liquid-handling protocols for formulating PVA-containing hydrogel arrays.
* `RFoptimo_1.py`, `RFoptimo_2.py`, `RFoptimo_3.py` : Batch synthesis protocols for the PEGDA/RF/TEA system split into 3 consecutive microplates (32 unique formulations with 3 replicates each).

### 3. High-Throughput Characterization & Data Analysis
* `measure.py`: Live data-acquisition and control script. Commands the Genmitsu 3018-PRO CNC framework via GRBL (G-Code), interface asynchronously with the Vernier Go Direct® force sensor, detects surfaces deterministically, and automatically fits raw curves to Hertzian contact mechanics (bulk range: 0.3–0.7 mm) while generating automated QC plots.

---

## Workflow Pipeline
1. Run the respective `LHS*.py` script to generate a non-overlapping, balanced chemical composition design space.
2. Load the resulting volumes into the `*optimo*.py` Opentrons protocols to execute autonomous microplate filling.
3. Cure the plates under UV and transfer them to the ASMI platform. Run `measure.py` to perform the 8-hour desatended mechanical mapping batch execution.

---

## Requirements & Installation

To run the design and characterization scripts locally, install the required scientific computing stack:

```bash
pip install numpy pandas scipy matplotlib openpyxl plotly pyserial
