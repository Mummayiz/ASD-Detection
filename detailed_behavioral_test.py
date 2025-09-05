#!/usr/bin/env python3
"""
Detailed Behavioral Assessment Test
Focus on verifying the prediction logic makes clinical sense
"""

import requests
import json

def test_behavioral_scenarios():
    base_url = "https://autism-scan.preview.emergentagent.com"
    
    scenarios = [
        {
            "name": "All High ASD (1s)",
            "data": {
                "A1_Score": 1, "A2_Score": 1, "A3_Score": 1, "A4_Score": 1, "A5_Score": 1,
                "A6_Score": 1, "A7_Score": 1, "A8_Score": 1, "A9_Score": 1, "A10_Score": 1,
                "age": 25.0, "gender": "m"
            },
            "expected": "HIGH"
        },
        {
            "name": "All Low ASD (0s)",
            "data": {
                "A1_Score": 0, "A2_Score": 0, "A3_Score": 0, "A4_Score": 0, "A5_Score": 0,
                "A6_Score": 0, "A7_Score": 0, "A8_Score": 0, "A9_Score": 0, "A10_Score": 0,
                "age": 30.0, "gender": "f"
            },
            "expected": "LOW"
        },
        {
            "name": "All Neutral (0.5s)",
            "data": {
                "A1_Score": 0.5, "A2_Score": 0.5, "A3_Score": 0.5, "A4_Score": 0.5, "A5_Score": 0.5,
                "A6_Score": 0.5, "A7_Score": 0.5, "A8_Score": 0.5, "A9_Score": 0.5, "A10_Score": 0.5,
                "age": 28.0, "gender": "m"
            },
            "expected": "MODERATE"
        },
        {
            "name": "Mixed High (7 high, 3 low)",
            "data": {
                "A1_Score": 1, "A2_Score": 1, "A3_Score": 1, "A4_Score": 1, "A5_Score": 1,
                "A6_Score": 1, "A7_Score": 1, "A8_Score": 0, "A9_Score": 0, "A10_Score": 0,
                "age": 22.0, "gender": "f"
            },
            "expected": "HIGH"
        },
        {
            "name": "Mixed Low (3 high, 7 low)",
            "data": {
                "A1_Score": 1, "A2_Score": 1, "A3_Score": 1, "A4_Score": 0, "A5_Score": 0,
                "A6_Score": 0, "A7_Score": 0, "A8_Score": 0, "A9_Score": 0, "A10_Score": 0,
                "age": 35.0, "gender": "m"
            },
            "expected": "LOW-MODERATE"
        }
    ]
    
    print("🔬 DETAILED BEHAVIORAL ASSESSMENT TESTING")
    print("=" * 60)
    
    results = []
    
    for scenario in scenarios:
        print(f"\n📋 Testing: {scenario['name']}")
        print(f"Expected: {scenario['expected']} ASD probability")
        
        try:
            response = requests.post(
                f"{base_url}/api/assessment/behavioral",
                json=scenario['data'],
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                probability = result.get('probability', 0)
                prediction = result.get('prediction', 0)
                
                print(f"   Prediction: {prediction} ({'ASD' if prediction == 1 else 'No ASD'})")
                print(f"   Probability: {probability:.6f}")
                
                # Analyze model results
                if 'model_results' in result:
                    mr = result['model_results']
                    if 'random_forest' in mr:
                        print(f"   RF Probability: {mr['random_forest']['probability']:.6f}")
                    if 'svm' in mr:
                        print(f"   SVM Probability: {mr['svm']['probability']:.6f}")
                    if 'pso' in mr:
                        print(f"   PSO Probability: {mr['pso']['probability']:.6f}")
                        print(f"   PSO Weights: {mr['pso']['weights']}")
                
                # Clinical assessment
                if scenario['expected'] == "HIGH" and probability > 0.7:
                    status = "✅ CORRECT"
                elif scenario['expected'] == "LOW" and probability < 0.3:
                    status = "✅ CORRECT"
                elif scenario['expected'] == "MODERATE" and 0.3 <= probability <= 0.7:
                    status = "✅ CORRECT"
                elif scenario['expected'] == "LOW-MODERATE" and probability < 0.6:
                    status = "✅ ACCEPTABLE"
                else:
                    status = "❌ UNEXPECTED"
                
                print(f"   Assessment: {status}")
                
                results.append({
                    'scenario': scenario['name'],
                    'probability': probability,
                    'prediction': prediction,
                    'expected': scenario['expected'],
                    'status': status
                })
                
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 BEHAVIORAL ASSESSMENT SUMMARY")
    print("=" * 60)
    
    for result in results:
        print(f"{result['scenario']:25} | Prob: {result['probability']:.3f} | Pred: {result['prediction']} | {result['status']}")
    
    # Check for prediction inversion
    high_results = [r for r in results if 'High' in r['scenario']]
    low_results = [r for r in results if 'Low' in r['scenario']]
    
    if high_results and low_results:
        avg_high = sum(r['probability'] for r in high_results) / len(high_results)
        avg_low = sum(r['probability'] for r in low_results) / len(low_results)
        
        print(f"\nAverage High ASD Probability: {avg_high:.3f}")
        print(f"Average Low ASD Probability: {avg_low:.3f}")
        
        if avg_high > avg_low:
            print("✅ PREDICTION LOGIC: Correct (High > Low)")
        else:
            print("❌ PREDICTION LOGIC: Inverted (High ≤ Low)")

if __name__ == "__main__":
    test_behavioral_scenarios()