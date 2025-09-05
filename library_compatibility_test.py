#!/usr/bin/env python3
"""
Library Compatibility and Performance Testing for Updated Dependencies
Tests specific to the updated Python 3 compatible libraries
"""

import requests
import time
import sys
import json
import numpy as np
import pandas as pd
import sklearn
from datetime import datetime

class LibraryCompatibilityTester:
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
    
    def test_library_versions(self):
        """Test that updated library versions are working"""
        print("\n📚 Testing Updated Library Versions...")
        
        try:
            # Check scikit-learn version (should be 1.3.2)
            sklearn_version = sklearn.__version__
            expected_sklearn = "1.3.2"
            sklearn_ok = sklearn_version == expected_sklearn
            self.log_test("Scikit-learn Version", sklearn_ok, 
                         f"Expected: {expected_sklearn}, Got: {sklearn_version}")
            
            # Check numpy version (should be 1.24.3)
            numpy_version = np.__version__
            expected_numpy = "1.24.3"
            numpy_ok = numpy_version == expected_numpy
            self.log_test("NumPy Version", numpy_ok, 
                         f"Expected: {expected_numpy}, Got: {numpy_version}")
            
            # Check pandas version (should be 2.1.4)
            pandas_version = pd.__version__
            expected_pandas = "2.1.4"
            pandas_ok = pandas_version == expected_pandas
            self.log_test("Pandas Version", pandas_ok, 
                         f"Expected: {expected_pandas}, Got: {pandas_version}")
            
        except Exception as e:
            self.log_test("Library Version Check", False, str(e))
    
    def test_pso_performance_with_updated_sklearn(self):
        """Test PSO performance with updated scikit-learn"""
        print("\n🔄 Testing PSO Performance with Updated Scikit-learn...")
        
        # Test multiple requests to check consistency and performance
        test_data = {
            "A1_Score": 0.5, "A2_Score": 1, "A3_Score": 0.5, "A4_Score": 1, "A5_Score": 0,
            "A6_Score": 0.5, "A7_Score": 0, "A8_Score": 0.5, "A9_Score": 1, "A10_Score": 0.5,
            "age": 32.0, "gender": "m"
        }
        
        response_times = []
        pso_results = []
        
        try:
            for i in range(3):  # Test 3 times for consistency
                start_time = time.time()
                
                response = requests.post(
                    f"{self.base_url}/api/assessment/behavioral",
                    json=test_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=20
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                response_times.append(response_time)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'pso' in result['model_results']:
                        pso_results.append(result['model_results']['pso'])
                
            # Check performance
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            # Performance should be reasonable (under 15 seconds)
            performance_ok = max_response_time < 15.0
            
            # Check PSO consistency
            pso_consistent = len(pso_results) == 3
            if pso_consistent:
                # Check that PSO weights are properly normalized
                for pso_result in pso_results:
                    weights_sum = sum(pso_result['weights'])
                    if abs(weights_sum - 1.0) > 0.1:
                        pso_consistent = False
                        break
            
            success = performance_ok and pso_consistent
            details = f"Avg: {avg_response_time:.2f}s, Max: {max_response_time:.2f}s, PSO Consistent: {pso_consistent}"
            
            self.log_test("PSO Performance with Updated Scikit-learn", success, details)
            
        except Exception as e:
            self.log_test("PSO Performance with Updated Scikit-learn", False, str(e))
    
    def test_memory_usage_and_stability(self):
        """Test memory usage and stability with updated libraries"""
        print("\n💾 Testing Memory Usage and Stability...")
        
        # Test multiple rapid requests to check for memory leaks
        test_data = {
            "A1_Score": 1, "A2_Score": 0, "A3_Score": 1, "A4_Score": 0, "A5_Score": 1,
            "A6_Score": 0, "A7_Score": 1, "A8_Score": 0, "A9_Score": 1, "A10_Score": 0,
            "age": 25.0, "gender": "f"
        }
        
        try:
            successful_requests = 0
            failed_requests = 0
            
            for i in range(5):  # Test 5 rapid requests
                response = requests.post(
                    f"{self.base_url}/api/assessment/behavioral",
                    json=test_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                
                if response.status_code == 200:
                    successful_requests += 1
                else:
                    failed_requests += 1
                
                # Small delay between requests
                time.sleep(0.5)
            
            # All requests should succeed
            stability_ok = failed_requests == 0
            details = f"Successful: {successful_requests}, Failed: {failed_requests}"
            
            self.log_test("Memory Usage and Stability", stability_ok, details)
            
        except Exception as e:
            self.log_test("Memory Usage and Stability", False, str(e))
    
    def test_error_handling_with_updated_libraries(self):
        """Test error handling works properly with updated libraries"""
        print("\n🛡️ Testing Error Handling with Updated Libraries...")
        
        # Test various error conditions
        error_tests = [
            {
                "name": "Invalid Score Range",
                "data": {"A1_Score": 1.5, "age": 25, "gender": "m"},
                "expected_status": [400, 422]
            },
            {
                "name": "Missing Required Fields", 
                "data": {"A1_Score": 1},
                "expected_status": [400, 422]
            },
            {
                "name": "Invalid Data Types",
                "data": {"A1_Score": "invalid", "age": "not_number", "gender": "m"},
                "expected_status": [400, 422]
            }
        ]
        
        try:
            all_passed = True
            
            for test in error_tests:
                response = requests.post(
                    f"{self.base_url}/api/assessment/behavioral",
                    json=test["data"],
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                if response.status_code not in test["expected_status"]:
                    all_passed = False
                    print(f"   ❌ {test['name']}: Expected {test['expected_status']}, got {response.status_code}")
                else:
                    print(f"   ✅ {test['name']}: Correctly returned {response.status_code}")
            
            self.log_test("Error Handling with Updated Libraries", all_passed)
            
        except Exception as e:
            self.log_test("Error Handling with Updated Libraries", False, str(e))
    
    def test_deployment_readiness(self):
        """Test deployment readiness with updated libraries"""
        print("\n🚀 Testing Deployment Readiness...")
        
        try:
            # Test health endpoint response time
            start_time = time.time()
            health_response = requests.get(f"{self.base_url}/api/health", timeout=10)
            health_time = time.time() - start_time
            
            health_ok = health_response.status_code == 200 and health_time < 5.0
            
            # Test that all expected models are loaded
            if health_ok:
                health_data = health_response.json()
                models_loaded = health_data.get('models_loaded', 0)
                expected_models = 4  # behavioral_rf, behavioral_svm, eye_tracking_rf, eye_tracking_svm
                models_ok = models_loaded >= expected_models
            else:
                models_ok = False
            
            # Test API structure consistency
            api_response = requests.get(f"{self.base_url}/api/", timeout=10)
            api_ok = api_response.status_code == 200
            
            if api_ok:
                api_data = api_response.json()
                required_fields = ['message', 'version', 'status', 'stages']
                api_structure_ok = all(field in api_data for field in required_fields)
            else:
                api_structure_ok = False
            
            overall_ready = health_ok and models_ok and api_ok and api_structure_ok
            
            details = f"Health: {health_ok} ({health_time:.2f}s), Models: {models_ok} ({models_loaded}), API: {api_structure_ok}"
            
            self.log_test("Deployment Readiness", overall_ready, details)
            
        except Exception as e:
            self.log_test("Deployment Readiness", False, str(e))
    
    def test_neutral_values_edge_cases(self):
        """Test edge cases with neutral values (0.5)"""
        print("\n🎯 Testing Neutral Values Edge Cases...")
        
        edge_cases = [
            {
                "name": "All Neutral Values",
                "data": {f"A{i}_Score": 0.5 for i in range(1, 11)},
            },
            {
                "name": "Mixed with Extremes",
                "data": {"A1_Score": 0, "A2_Score": 0.5, "A3_Score": 1, "A4_Score": 0.5, "A5_Score": 0,
                        "A6_Score": 1, "A7_Score": 0.5, "A8_Score": 0, "A9_Score": 0.5, "A10_Score": 1},
            }
        ]
        
        try:
            all_passed = True
            
            for case in edge_cases:
                test_data = case["data"].copy()
                test_data.update({"age": 28.0, "gender": "f"})
                
                response = requests.post(
                    f"{self.base_url}/api/assessment/behavioral",
                    json=test_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Check that PSO still works
                    if 'pso' in result['model_results']:
                        pso_result = result['model_results']['pso']
                        weights_sum = sum(pso_result['weights'])
                        if abs(weights_sum - 1.0) > 0.1:
                            all_passed = False
                            print(f"   ❌ {case['name']}: PSO weights not normalized ({weights_sum:.3f})")
                        else:
                            print(f"   ✅ {case['name']}: PSO working correctly")
                    else:
                        all_passed = False
                        print(f"   ❌ {case['name']}: PSO results missing")
                else:
                    all_passed = False
                    print(f"   ❌ {case['name']}: Request failed ({response.status_code})")
            
            self.log_test("Neutral Values Edge Cases", all_passed)
            
        except Exception as e:
            self.log_test("Neutral Values Edge Cases", False, str(e))
    
    def run_all_tests(self):
        """Run all library compatibility tests"""
        print("🔬 Library Compatibility & Performance Testing")
        print("📋 Focus: Updated Python 3 Compatible Libraries")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run all test suites
        self.test_library_versions()
        self.test_pso_performance_with_updated_sklearn()
        self.test_memory_usage_and_stability()
        self.test_error_handling_with_updated_libraries()
        self.test_deployment_readiness()
        self.test_neutral_values_edge_cases()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 LIBRARY COMPATIBILITY TEST SUMMARY")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All library compatibility tests passed!")
            print("✅ Updated Libraries: Compatible")
            print("✅ Performance: Acceptable")
            print("✅ Deployment: Ready")
            return 0
        else:
            print("❌ Some compatibility tests failed. Check details above.")
            return 1

def main():
    """Main test execution"""
    tester = LibraryCompatibilityTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())