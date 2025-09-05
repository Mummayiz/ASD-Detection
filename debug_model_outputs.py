#!/usr/bin/env python3
"""
Debug model outputs to understand the unexpected behavior
"""

import requests
import json

def test_extreme_cases():
    base_url = "https://autism-scan.preview.emergentagent.com"
    
    print("🔍 Debugging Model Output Issues...")
    
    # Test case 1: All high ASD indicators (should give high probability)
    high_asd_data = {
        "A1_Score": 1, "A2_Score": 1, "A3_Score": 1, "A4_Score": 1, "A5_Score": 1,
        "A6_Score": 1, "A7_Score": 1, "A8_Score": 1, "A9_Score": 1, "A10_Score": 1,
        "age": 25.0, "gender": "f"
    }
    
    print("\n📊 Testing All High ASD Indicators (all 1s):")
    response = requests.post(
        f"{base_url}/api/assessment/behavioral",
        json=high_asd_data,
        headers={'Content-Type': 'application/json'},
        timeout=15
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Prediction: {result['prediction']}")
        print(f"   Probability: {result['probability']:.6f}")
        print(f"   Confidence: {result['confidence']:.6f}")
        print(f"   RF Prob: {result['model_results']['random_forest']['probability']:.6f}")
        print(f"   SVM Prob: {result['model_results']['svm']['probability']:.6f}")
        if 'pso' in result['model_results']:
            pso = result['model_results']['pso']
            print(f"   PSO Prob: {pso['probability']:.6f}")
            print(f"   PSO Weights: {pso['weights']}")
    else:
        print(f"   Request failed: {response.status_code}")
    
    # Test case 2: All low ASD indicators (should give low probability)
    low_asd_data = {
        "A1_Score": 0, "A2_Score": 0, "A3_Score": 0, "A4_Score": 0, "A5_Score": 0,
        "A6_Score": 0, "A7_Score": 0, "A8_Score": 0, "A9_Score": 0, "A10_Score": 0,
        "age": 25.0, "gender": "f"
    }
    
    print("\n📊 Testing All Low ASD Indicators (all 0s):")
    response = requests.post(
        f"{base_url}/api/assessment/behavioral",
        json=low_asd_data,
        headers={'Content-Type': 'application/json'},
        timeout=15
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Prediction: {result['prediction']}")
        print(f"   Probability: {result['probability']:.6f}")
        print(f"   Confidence: {result['confidence']:.6f}")
        print(f"   RF Prob: {result['model_results']['random_forest']['probability']:.6f}")
        print(f"   SVM Prob: {result['model_results']['svm']['probability']:.6f}")
        if 'pso' in result['model_results']:
            pso = result['model_results']['pso']
            print(f"   PSO Prob: {pso['probability']:.6f}")
            print(f"   PSO Weights: {pso['weights']}")
    else:
        print(f"   Request failed: {response.status_code}")
    
    # Test case 3: Mixed case that worked
    mixed_data = {
        "A1_Score": 1, "A2_Score": 0, "A3_Score": 1, "A4_Score": 0, "A5_Score": 1,
        "A6_Score": 0, "A7_Score": 1, "A8_Score": 0, "A9_Score": 1, "A10_Score": 0,
        "age": 25.0, "gender": "f"
    }
    
    print("\n📊 Testing Mixed Indicators (worked correctly):")
    response = requests.post(
        f"{base_url}/api/assessment/behavioral",
        json=mixed_data,
        headers={'Content-Type': 'application/json'},
        timeout=15
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Prediction: {result['prediction']}")
        print(f"   Probability: {result['probability']:.6f}")
        print(f"   Confidence: {result['confidence']:.6f}")
        print(f"   RF Prob: {result['model_results']['random_forest']['probability']:.6f}")
        print(f"   SVM Prob: {result['model_results']['svm']['probability']:.6f}")
        if 'pso' in result['model_results']:
            pso = result['model_results']['pso']
            print(f"   PSO Prob: {pso['probability']:.6f}")
            print(f"   PSO Weights: {pso['weights']}")
    else:
        print(f"   Request failed: {response.status_code}")

if __name__ == "__main__":
    test_extreme_cases()