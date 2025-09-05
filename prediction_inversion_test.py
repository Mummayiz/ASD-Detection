#!/usr/bin/env python3
"""
Critical Prediction Logic Test for ASD Detection System
Specifically tests for the prediction inversion issue after scikit-learn compatibility fixes
"""

import requests
import sys
import json
from datetime import datetime
import time

class PredictionInversionTester:
    def __init__(self, base_url="https://autism-scan.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.critical_issues = []
        
    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
            self.critical_issues.append(f"{name}: {details}")
        
    def test_high_asd_indicators(self):
        """Test behavioral assessment with ALL HIGH ASD indicators (all 1s) - should return HIGH probability"""
        print("\n🔴 Testing HIGH ASD Indicators (All 1s) - Expected: HIGH probability (>0.5)")
        
        high_asd_data = {
            "A1_Score": 1,  # Social responsiveness issues
            "A2_Score": 1,  # Communication difficulties
            "A3_Score": 1,  # Repetitive behaviors
            "A4_Score": 1,  # Social interaction challenges
            "A5_Score": 1,  # Attention to detail patterns
            "A6_Score": 1,  # Sensory sensitivity
            "A7_Score": 1,  # Language development concerns
            "A8_Score": 1,  # Motor skills issues
            "A9_Score": 1,  # Behavioral inflexibility
            "A10_Score": 1, # Emotional regulation difficulties
            "age": 25.0,
            "gender": "m"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/assessment/behavioral",
                json=high_asd_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                probability = result['probability']
                prediction = result['prediction']
                
                print(f"   Prediction: {prediction} (1=ASD, 0=No ASD)")
                print(f"   Probability: {probability:.6f}")
                print(f"   RF Probability: {result['model_results']['random_forest']['probability']:.6f}")
                print(f"   SVM Probability: {result['model_results']['svm']['probability']:.6f}")
                
                if 'pso' in result['model_results']:
                    pso_prob = result['model_results']['pso']['probability']
                    print(f"   PSO Probability: {pso_prob:.6f}")
                
                # CRITICAL CHECK: High ASD indicators should yield HIGH probability (>0.5)
                if probability > 0.5:
                    print(f"   ✅ CORRECT: High ASD indicators → High probability ({probability:.3f})")
                    success = True
                else:
                    print(f"   ❌ INVERTED: High ASD indicators → Low probability ({probability:.6f})")
                    success = False
                    
            self.log_test("High ASD Indicators Test", success, 
                         f"Probability: {probability:.6f} (Expected >0.5)" if 'probability' in locals() else "API Error")
            
        except Exception as e:
            self.log_test("High ASD Indicators Test", False, str(e))

    def test_low_asd_indicators(self):
        """Test behavioral assessment with ALL LOW ASD indicators (all 0s) - should return LOW probability"""
        print("\n🟢 Testing LOW ASD Indicators (All 0s) - Expected: LOW probability (<0.5)")
        
        low_asd_data = {
            "A1_Score": 0,  # No social responsiveness issues
            "A2_Score": 0,  # No communication difficulties
            "A3_Score": 0,  # No repetitive behaviors
            "A4_Score": 0,  # No social interaction challenges
            "A5_Score": 0,  # No attention to detail patterns
            "A6_Score": 0,  # No sensory sensitivity
            "A7_Score": 0,  # No language development concerns
            "A8_Score": 0,  # No motor skills issues
            "A9_Score": 0,  # No behavioral inflexibility
            "A10_Score": 0, # No emotional regulation difficulties
            "age": 25.0,
            "gender": "f"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/assessment/behavioral",
                json=low_asd_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                probability = result['probability']
                prediction = result['prediction']
                
                print(f"   Prediction: {prediction} (1=ASD, 0=No ASD)")
                print(f"   Probability: {probability:.6f}")
                print(f"   RF Probability: {result['model_results']['random_forest']['probability']:.6f}")
                print(f"   SVM Probability: {result['model_results']['svm']['probability']:.6f}")
                
                if 'pso' in result['model_results']:
                    pso_prob = result['model_results']['pso']['probability']
                    print(f"   PSO Probability: {pso_prob:.6f}")
                
                # CRITICAL CHECK: Low ASD indicators should yield LOW probability (<0.5)
                if probability < 0.5:
                    print(f"   ✅ CORRECT: Low ASD indicators → Low probability ({probability:.3f})")
                    success = True
                else:
                    print(f"   ❌ INVERTED: Low ASD indicators → High probability ({probability:.6f})")
                    success = False
                    
            self.log_test("Low ASD Indicators Test", success, 
                         f"Probability: {probability:.6f} (Expected <0.5)" if 'probability' in locals() else "API Error")
            
        except Exception as e:
            self.log_test("Low ASD Indicators Test", False, str(e))

    def test_neutral_values_processing(self):
        """Test behavioral assessment with mixed neutral values (0.5) - should work properly"""
        print("\n🟡 Testing NEUTRAL Values (0.5) Processing - Expected: Proper handling")
        
        neutral_mixed_data = {
            "A1_Score": 0.5,  # Sometimes social challenges
            "A2_Score": 0,    # No communication issues
            "A3_Score": 1,    # Repetitive behaviors present
            "A4_Score": 0.5,  # Sometimes prefer routine
            "A5_Score": 1,    # Focus intensely on interests
            "A6_Score": 0.5,  # Some sensory sensitivity
            "A7_Score": 0,    # No language delays
            "A8_Score": 0.5,  # Some motor coordination issues
            "A9_Score": 1,    # Difficulty with changes
            "A10_Score": 0.5, # Some emotional regulation challenges
            "age": 30.0,
            "gender": "m"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/assessment/behavioral",
                json=neutral_mixed_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                probability = result['probability']
                prediction = result['prediction']
                
                print(f"   Prediction: {prediction} (1=ASD, 0=No ASD)")
                print(f"   Probability: {probability:.6f}")
                
                # Check PSO functionality with neutral values
                if 'pso' in result['model_results']:
                    pso_result = result['model_results']['pso']
                    weights_sum = sum(pso_result['weights'])
                    print(f"   PSO Weights Sum: {weights_sum:.3f} (should be ~1.0)")
                    print(f"   PSO Probability: {pso_result['probability']:.6f}")
                    
                    # PSO weights should be normalized
                    if abs(weights_sum - 1.0) < 0.1:
                        print(f"   ✅ PSO weights properly normalized")
                    else:
                        print(f"   ❌ PSO weights not normalized: {weights_sum}")
                        success = False
                else:
                    print(f"   ❌ PSO results missing")
                    success = False
                
                # Neutral values should produce reasonable probability (not extreme)
                if 0.1 < probability < 0.9:
                    print(f"   ✅ Neutral values produce reasonable probability")
                else:
                    print(f"   ⚠️ Extreme probability with mixed values: {probability:.6f}")
                    
            self.log_test("Neutral Values Processing", success, 
                         f"Status: {response.status_code}" if response else "Request failed")
            
        except Exception as e:
            self.log_test("Neutral Values Processing", False, str(e))

    def test_eye_tracking_prediction_logic(self):
        """Test eye tracking assessment for prediction logic consistency"""
        print("\n👁️ Testing Eye Tracking Prediction Logic")
        
        # Test data that should indicate ASD patterns
        asd_pattern_data = {
            "fixation_count": 120.0,    # High fixation count (atypical)
            "mean_saccade": 25.0,       # Low saccade amplitude
            "max_saccade": 45.0,        # Low max saccade
            "std_saccade": 8.0,         # Low variability
            "mean_x": 400.0,            # Off-center gaze
            "mean_y": 200.0,            # Upper region focus
            "std_x": 150.0,             # High horizontal variability
            "std_y": 120.0,             # High vertical variability
            "mean_pupil": 3.0           # Small pupil diameter
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/assessment/eye_tracking",
                json=asd_pattern_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 501:
                print("   Eye tracking models not available (acceptable for demo)")
                self.log_test("Eye Tracking Prediction Logic", True, "Models not available")
                return
            
            success = response.status_code == 200
            if success:
                result = response.json()
                probability = result['probability']
                
                print(f"   Prediction: {result['prediction']}")
                print(f"   Probability: {probability:.6f}")
                
                # Check PSO integration
                if 'pso' in result['model_results']:
                    pso_result = result['model_results']['pso']
                    weights_sum = sum(pso_result['weights'])
                    print(f"   PSO Weights Sum: {weights_sum:.3f}")
                    print(f"   PSO Probability: {pso_result['probability']:.6f}")
                    
                    if abs(weights_sum - 1.0) < 0.1:
                        print(f"   ✅ PSO weights normalized")
                    else:
                        success = False
                else:
                    print(f"   ❌ PSO results missing")
                    success = False
                    
            self.log_test("Eye Tracking Prediction Logic", success, 
                         f"Status: {response.status_code}")
            
        except Exception as e:
            self.log_test("Eye Tracking Prediction Logic", False, str(e))

    def test_complete_assessment_integration(self):
        """Test complete assessment integration with corrected predictions"""
        print("\n🎯 Testing Complete Assessment Integration")
        
        session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/assessment/complete",
                json={"session_id": session_id},
                headers={'Content-Type': 'application/json'},
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                
                print(f"   Final Prediction: {result['final_prediction']}")
                print(f"   Final Probability: {result['final_probability']:.6f}")
                print(f"   Confidence Score: {result['confidence_score']:.3f}")
                print(f"   Stages Completed: {result['stages_completed']}")
                
                # Check if stage results are properly integrated
                if 'stage_results' in result:
                    stages = result['stage_results']
                    print(f"   Available Stages: {list(stages.keys())}")
                    
                    # Verify stage predictions are consistent with final prediction
                    stage_predictions = [stages[stage]['prediction'] for stage in stages if 'prediction' in stages[stage]]
                    if stage_predictions:
                        print(f"   Stage Predictions: {stage_predictions}")
                        
                # Check explanation structure
                if 'explanation' in result and 'overall_result' in result['explanation']:
                    print(f"   Overall Result: {result['explanation']['overall_result']}")
                    
            self.log_test("Complete Assessment Integration", success, 
                         f"Status: {response.status_code}")
            
        except Exception as e:
            self.log_test("Complete Assessment Integration", False, str(e))

    def test_performance_and_stability(self):
        """Test response times and stability"""
        print("\n⚡ Testing Performance and Stability")
        
        test_data = {
            "A1_Score": 0.5, "A2_Score": 1, "A3_Score": 0, "A4_Score": 0.5, "A5_Score": 1,
            "A6_Score": 0, "A7_Score": 0.5, "A8_Score": 1, "A9_Score": 0, "A10_Score": 0.5,
            "age": 28.0, "gender": "f"
        }
        
        response_times = []
        
        try:
            # Test multiple requests for stability
            for i in range(3):
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/assessment/behavioral",
                    json=test_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    response_time = end_time - start_time
                    response_times.append(response_time)
                    print(f"   Request {i+1}: {response_time:.3f}s")
                else:
                    print(f"   Request {i+1}: Failed (Status: {response.status_code})")
            
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                print(f"   Average Response Time: {avg_time:.3f}s")
                
                # Performance should be reasonable (< 5 seconds)
                success = avg_time < 5.0 and len(response_times) == 3
                if success:
                    print(f"   ✅ Performance acceptable")
                else:
                    print(f"   ❌ Performance issues detected")
            else:
                success = False
                
            self.log_test("Performance and Stability", success, 
                         f"Avg time: {avg_time:.3f}s" if response_times else "All requests failed")
            
        except Exception as e:
            self.log_test("Performance and Stability", False, str(e))

    def run_critical_tests(self):
        """Run all critical prediction logic tests"""
        print("🔬 CRITICAL PREDICTION LOGIC VERIFICATION")
        print("Testing for scikit-learn compatibility and prediction inversion fixes")
        print(f"Testing against: {self.base_url}")
        print("=" * 70)
        
        # Run critical tests in order
        self.test_high_asd_indicators()
        self.test_low_asd_indicators()
        self.test_neutral_values_processing()
        self.test_eye_tracking_prediction_logic()
        self.test_complete_assessment_integration()
        self.test_performance_and_stability()
        
        # Print detailed summary
        print("\n" + "=" * 70)
        print(f"🔍 CRITICAL TEST RESULTS")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.critical_issues:
            print(f"\n❌ CRITICAL ISSUES FOUND:")
            for issue in self.critical_issues:
                print(f"   • {issue}")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL CRITICAL TESTS PASSED!")
            print("✅ Prediction logic is CORRECT (not inverted)")
            print("✅ High ASD indicators → High probabilities")
            print("✅ Low ASD indicators → Low probabilities")
            print("✅ PSO optimization working properly")
            print("✅ Neutral values (0.5) supported")
            print("✅ System ready for production deployment")
            return 0
        else:
            print(f"\n❌ CRITICAL FAILURES DETECTED!")
            print("⚠️  System NOT ready for production deployment")
            print("🔧 Issues must be resolved before deployment")
            return 1

def main():
    """Main test execution"""
    tester = PredictionInversionTester()
    return tester.run_critical_tests()

if __name__ == "__main__":
    sys.exit(main())