# PubChem Jaccard Optimization System

## Overview
This project implements a scalable similarity computation framework for large molecular datasets. It focuses on optimizing Jaccard (Tanimoto-style) similarity calculations using pre-filtering techniques and a custom weighted similarity method to improve both efficiency and matching quality.

## Problem
Standard pairwise similarity computation is computationally expensive for large datasets due to its quadratic complexity. When applied to large molecular datasets (e.g., PubChem-scale data), brute-force comparison becomes infeasible.

## Solution
This project addresses the problem using two main improvements:

### 1. Pre-filtering (Bucketizing Approach)
- Reduces number of candidate comparisons
- Groups molecules into buckets based on shared fingerprint characteristics
- Avoids unnecessary full pairwise similarity computation

### 2. Weighted Similarity Method ("Willems Method")
- Extends traditional Jaccard/Tanimoto similarity
- Assigns weights to specific fingerprint positions
- Improves sensitivity to important structural differences

## System Components
- `bucketizing/` → Pre-filtering and candidate reduction logic
- `brute_force/` → Baseline similarity computation for comparison
- `benchmark/` → Performance evaluation scripts
- `tanimoto.py` → Standard similarity calculation
- `Willems.py` → Weighted similarity implementation

## Setup

It is recommended to run this project inside a virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install pandas

## How to Run
Generate the dataset:
python3 generate_small_dataset.py

Run full benchmark:
python3 benchmark/run_benchmark.py

Run similarity comparison:
python3 benchmark/run_benchmark_similarity.py

## Dataset Notes
Large PubChem-scale datasets are not included due to size constraints. A synthetic dataset generator is provided for testing and benchmarking purposes.

## Results
The optimized pipeline reduces computation time compared to brute-force similarity while maintaining meaningful similarity accuracy through weighted scoring and pre-filtering.

## Technologies
- Python
- Pandas
- NumPy
- Custom molecular fingerprint processing

## Author
Orry Willems
