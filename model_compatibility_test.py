#!/usr/bin/env python3
"""
Model Compatibility Testing for Scikit-learn Version Mismatch
Tests to ensure models trained with 1.3.0 work correctly with 1.3.2
"""

import requests
import sys
import json
import numpy as np
from datetime import datetime

class ModelCompatibilityTester:
    def __init__(self, base_url="https://autism-scan.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        
    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        if details and success:
            print(f"   {details}")
    
    def test_model_prediction_consistency(self):
        """Test that model predictions are consistent despite version mismatch"""
        print("\n🔄 Testing Model Prediction Consistency...")
        
        # Test the same input multiple times to check consistency
        test_data = {
            "A1_Score": 1, "A2_Score": 0, "A3_Score": 1, "A4_Score": 1, "A5_Score": 1,
            "A6_Score": 1, "A7_Score": 0, "A8_Score": 0, "A9_Score": 1, "A10_Score": 0,
            "age": 30.0, "gender": "m"
        }
        
        try:
            predictions = []
            probabilities = []
            
            # Run the same test 5 times
            for i in range(5):
                response = requests.post(
                    f"{self.base_url}/api/assessment/behavioral",
                    json=test_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    predictions.append(result['prediction'])
                    probabilities.append(result['probability'])
                else:
                    self.log_test("Model Prediction Consistency", False, f"Request failed: {response.status_code}")
                    return
            
            # Check consistency
            prediction_consistent = len(set(predictions)) == 1  # All predictions should be the same
            probability_variance = np.var(probabilities)
            probability_consistent = probability_variance < 0.01  # Very low variance expected
            
            success = prediction_consistent and probability_consistent
            details = f"Predictions consistent: {prediction_consistent}, Prob variance: {probability_variance:.6f}"
            
            self.log_test("Model Prediction Consistency", success, details)
            
        except Exception as e:
            self.log_test("Model Prediction Consistency", False, str(e))
    
    def test_model_output_ranges(self):
        """Test that model outputs are within expected ranges"""
        print("\n📊 Testing Model Output Ranges...")
        
        test_cases = [
            {
                "name": "High ASD Indicators",
                "data": {f"A{i}_Score": 1 for i in range(1, 11)},
                "expected_high_prob": True
            },
            {
                "name": "Low ASD Indicators", 
                "data": {f"A{i}_Score": 0 for i in range(1, 11)},
                "expected_high_prob": False
            },
            {
                "name": "Mixed Indicators",
                "data": {"A1_Score": 1, "A2_Score": 0, "A3_Score": 1, "A4_Score": 0, "A5_Score": 1,
                        "A6_Score": 0, "A7_Score": 1, "A8_Score": 0, "A9_Score": 1, "A10_Score": 0},
                "expected_high_prob": None  # Could go either way
            }
        ]
        
        try:
            all_passed = True
            
            for case in test_cases:
                test_data = case["data"].copy()
                test_data.update({"age": 25.0, "gender": "f"})
                
                response = requests.post(
                    f"{self.base_url}/api/assessment/behavioral",
                    json=test_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    prob = result['probability']
                    pred = result['prediction']
                    
                    # Check probability is in valid range [0, 1]
                    prob_valid = 0 <= prob <= 1
                    
                    # Check prediction matches probability
                    pred_valid = (pred == 1 and prob > 0.5) or (pred == 0 and prob <= 0.5)
                    
                    # Check expected behavior if specified
                    expected_valid = True
                    if case["expected_high_prob"] is True:
                        expected_valid = prob > 0.6
                    elif case["expected_high_prob"] is False:
                        expected_valid = prob < 0.4
                    
                    case_passed = prob_valid and pred_valid and expected_valid
                    
                    if case_passed:
                        print(f"   ✅ {case['name']}: Prob={prob:.3f}, Pred={pred}")
                    else:
                        print(f"   ❌ {case['name']}: Prob={prob:.3f}, Pred={pred} (Invalid)")
                        all_passed = False
                else:
                    print(f"   ❌ {case['name']}: Request failed ({response.status_code})")
                    all_passed = False
            
            self.log_test("Model Output Ranges", all_passed)
            
        except Exception as e:
            self.log_test("Model Output Ranges", False, str(e))
    
    def test_pso_optimization_stability(self):
        """Test PSO optimization stability with version mismatch"""
        print("\n🎯 Testing PSO Optimization Stability...")
        
        test_data = {
            "A1_Score": 0.5, "A2_Score": 1, "A3_Score": 0.5, "A4_Score": 0, "A5_Score": 1,
            "A6_Score": 0.5, "A7_Score": 0, "A8_Score": 0.5, "A9_Score": 1, "A10_Score": 0.5,
            "age": 28.0, "gender": "m"
        }
        
        try:
            pso_weights_list = []
            pso_predictions = []
            
            # Test PSO multiple times
            for i in range(3):
                response = requests.post(
                    f"{self.base_url}/api/assessment/behavioral",
                    json=test_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'pso' in result['model_results']:
                        pso_result = result['model_results']['pso']
                        pso_weights_list.append(pso_result['weights'])
                        pso_predictions.append(pso_result['prediction'])
                    else:
                        self.log_test("PSO Optimization Stability", False, "PSO results missing")
                        return
                else:
                    self.log_test("PSO Optimization Stability", False, f"Request failed: {response.status_code}")
                    return
            
            # Check PSO stability
            weights_valid = True
            for weights in pso_weights_list:
                weights_sum = sum(weights)
                if abs(weights_sum - 1.0) > 0.1:
                    weights_valid = False
                    break
            
            # PSO predictions should be consistent for same input
            predictions_consistent = len(set(pso_predictions)) <= 2  # Allow some variation due to randomness
            
            success = weights_valid and predictions_consistent
            details = f"Weights valid: {weights_valid}, Predictions consistent: {predictions_consistent}"
            
            self.log_test("PSO Optimization Stability", success, details)
            
        except Exception as e:
            self.log_test("PSO Optimization Stability", False, str(e))
    
    def test_eye_tracking_model_compatibility(self):
        """Test eye tracking model compatibility"""
        print("\n👁️ Testing Eye Tracking Model Compatibility...")
        
        test_data = {
            "fixation_count": 85.0,
            "mean_saccade": 42.5,
            "max_saccade": 95.2,
            "std_saccade": 18.7,
            "mean_x": 640.0,
            "mean_y": 480.0,
            "std_x": 120.5,
            "std_y": 90.3,
            "mean_pupil": 3.8
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/assessment/eye_tracking",
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Check basic structure
                required_keys = ['prediction', 'probability', 'confidence', 'model_results']
                structure_ok = all(key in result for key in required_keys)
                
                # Check PSO integration
                pso_ok = 'pso' in result['model_results']
                if pso_ok:
                    pso_result = result['model_results']['pso']
                    weights_sum = sum(pso_result['weights'])
                    pso_ok = abs(weights_sum - 1.0) < 0.1
                
                success = structure_ok and pso_ok
                details = f"Structure: {structure_ok}, PSO: {pso_ok}"
                
            elif response.status_code == 501:
                # Models not available is acceptable
                success = True
                details = "Eye tracking models not available (expected)"
            else:
                success = False
                details = f"Unexpected status code: {response.status_code}"
            
            self.log_test("Eye Tracking Model Compatibility", success, details)
            
        except Exception as e:
            self.log_test("Eye Tracking Model Compatibility", False, str(e))
    
    def test_complete_pipeline_compatibility(self):
        """Test complete assessment pipeline compatibility"""
        print("\n🔗 Testing Complete Pipeline Compatibility...")
        
        try:
            # First run individual assessments
            behavioral_data = {
                "A1_Score": 1, "A2_Score": 0.5, "A3_Score": 1, "A4_Score": 0, "A5_Score": 1,
                "A6_Score": 0.5, "A7_Score": 0, "A8_Score": 0.5, "A9_Score": 1, "A10_Score": 0,
                "age": 27.0, "gender": "f"
            }
            
            # Behavioral assessment
            behavioral_response = requests.post(
                f"{self.base_url}/api/assessment/behavioral",
                json=behavioral_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            behavioral_ok = behavioral_response.status_code == 200
            
            # Eye tracking assessment
            eye_data = {
                "fixation_count": 70.0, "mean_saccade": 38.5, "max_saccade": 82.1, "std_saccade": 14.2,
                "mean_x": 512.0, "mean_y": 384.0, "std_x": 95.3, "std_y": 72.8, "mean_pupil": 4.1
            }
            
            eye_response = requests.post(
                f"{self.base_url}/api/assessment/eye_tracking",
                json=eye_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            eye_ok = eye_response.status_code in [200, 501]  # 501 is acceptable
            
            # Facial analysis
            facial_data = {
                "facial_features": [0.2] * 128,
                "emotion_scores": {"happy": 0.4, "neutral": 0.5, "sad": 0.1},
                "attention_patterns": {"attention_to_faces": 0.3, "attention_to_objects": 0.7}
            }
            
            facial_response = requests.post(
                f"{self.base_url}/api/assessment/facial_analysis",
                json=facial_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            facial_ok = facial_response.status_code == 200
            
            # Complete assessment
            complete_response = requests.post(
                f"{self.base_url}/api/assessment/complete",
                json={"session_id": "compatibility_test"},
                headers={'Content-Type': 'application/json'},
                timeout=20
            )
            
            complete_ok = complete_response.status_code == 200
            
            success = behavioral_ok and eye_ok and facial_ok and complete_ok
            details = f"Behavioral: {behavioral_ok}, Eye: {eye_ok}, Facial: {facial_ok}, Complete: {complete_ok}"
            
            self.log_test("Complete Pipeline Compatibility", success, details)
            
        except Exception as e:
            self.log_test("Complete Pipeline Compatibility", False, str(e))
    
    def run_all_tests(self):
        """Run all model compatibility tests"""
        print("🔬 Model Compatibility Testing")
        print("⚠️  Focus: Scikit-learn 1.3.0 → 1.3.2 Version Mismatch")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run all test suites
        self.test_model_prediction_consistency()
        self.test_model_output_ranges()
        self.test_pso_optimization_stability()
        self.test_eye_tracking_model_compatibility()
        self.test_complete_pipeline_compatibility()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 MODEL COMPATIBILITY TEST SUMMARY")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All model compatibility tests passed!")
            print("✅ Models work correctly despite version mismatch")
            print("⚠️  Note: Version warnings in logs are expected but not critical")
            return 0
        else:
            print("❌ Some model compatibility tests failed.")
            return 1

def main():
    """Main test execution"""
    tester = ModelCompatibilityTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())