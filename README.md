# PubChem Jaccard Optimization System

## Overview
This project implements a scalable similarity computation framework for large molecular datasets. It focuses on optimizing Jaccard (Tanimoto-style) similarity calculations using pre-filtering techniques and a custom weighted similarity method to improve both efficiency and matching quality.

## Problem
Standard pairwise similarity computation is computationally expensive for large datasets due to its quadratic complexity. When applied to large molecular datasets (e.g., PubChem-scale data), brute-force comparison becomes infeasible.

## Solution
This project addresses the problem using two main improvements:

### 1. Pre-filtering (Bucketizing Approach)
- Reduces the number of candidate comparisons
- Groups molecules into buckets based on shared characteristics
- Avoids unnecessary full pairwise similarity calculations

### 2. Weighted Similarity Method ("Willems Method")
- Extends traditional Jaccard/Tanimoto similarity
- Assigns different weights to specific positions/features in molecular representations
- Improves sensitivity to important structural differences

## System Components
- `bucketizing/` → Pre-filtering and candidate reduction logic  
- `brute_force/` → Baseline similarity computation for comparison  
- `benchmark/` → Performance evaluation scripts  
- `tanimoto.py` → Standard similarity calculations  
- `Willems.py` → Weighted similarity implementation  

## Results
The optimized pipeline significantly reduces computation time compared to brute-force similarity while maintaining meaningful similarity comparisons through weighted scoring.

## Notes
Large datasets are not included in this repository due to size constraints. The system is designed to scale to PubChem-level datasets and can be tested using generated or sampled data.

## Technologies
- Python
- NumPy
- Data processing pipelines for molecular fingerprints
