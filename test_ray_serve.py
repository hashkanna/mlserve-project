#!/usr/bin/env python3
"""Test script for Ray Serve integration."""

import requests
import json
import time
import sys


def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get("http://localhost:8000/api/v1/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_ray_status():
    """Test Ray status endpoint."""
    print("\nTesting Ray status endpoint...")
    response = requests.get("http://localhost:8000/api/v1/ray/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_list_models():
    """Test list models endpoint."""
    print("\nTesting list models endpoint...")
    response = requests.get("http://localhost:8000/api/v1/models")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_prediction():
    """Test prediction endpoint."""
    print("\nTesting prediction endpoint...")
    
    # Create smaller dummy image data - flatten format
    # ResNet expects (batch, channels, height, width) but we'll send a simple flat array
    dummy_data = [0.5] * 100  # Simplified dummy data
    
    payload = {
        "model": "resnet18",
        "data": [dummy_data]  # Batch of 1
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/predict",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Model: {result['model']}")
        print(f"Predictions: {json.dumps(result['predictions'][0], indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def test_concurrent_requests():
    """Test concurrent requests to trigger autoscaling."""
    print("\nTesting concurrent requests (check Ray Dashboard for scaling)...")
    
    import concurrent.futures
    
    def make_request(i):
        dummy_data = [0.5] * 100  # Simplified dummy data
        payload = {"model": "resnet18", "data": [dummy_data]}
        
        start = time.time()
        response = requests.post("http://localhost:8000/api/v1/predict", json=payload)
        end = time.time()
        
        return i, response.status_code, end - start
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, i) for i in range(20)]
        
        for future in concurrent.futures.as_completed(futures):
            i, status, duration = future.result()
            print(f"Request {i}: Status {status}, Duration {duration:.2f}s")


def main():
    """Run all tests."""
    print("Ray Serve Integration Test Suite")
    print("=" * 50)
    
    # Wait for services to be ready
    print("Waiting for services to start...")
    time.sleep(5)
    
    tests = [
        ("Health Check", test_health),
        ("Ray Status", test_ray_status),
        ("List Models", test_list_models),
        ("Prediction", test_prediction),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"Error in {name}: {e}")
            results.append((name, False))
    
    # Run concurrent test separately
    print("\n" + "=" * 50)
    try:
        test_concurrent_requests()
    except Exception as e:
        print(f"Error in concurrent test: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    for name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"  {name}: {status}")
    
    # Check Ray Dashboard
    print("\n" + "=" * 50)
    print("Check Ray Dashboard at: http://localhost:8265")
    print("Look for:")
    print("  - Cluster resources")
    print("  - Deployment status")
    print("  - Autoscaling behavior")
    print("  - Request metrics")


if __name__ == "__main__":
    main()