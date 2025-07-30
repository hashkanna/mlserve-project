#!/usr/bin/env python3
"""Quick demo script to test the UI functionality."""

import requests
import json
import time

def test_api_endpoints():
    """Test all API endpoints to ensure they work."""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 Testing API Endpoints...")
    print("-" * 40)
    
    # Test health
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health: {e}")
    
    # Test models
    try:
        response = requests.get(f"{base_url}/models")
        print(f"✅ Models: {response.status_code}")
        models = response.json()['models']
        for model in models:
            print(f"   📦 {model['name']} - {model['status']}")
    except Exception as e:
        print(f"❌ Models: {e}")
    
    # Test prediction with exact same payload as UI
    try:
        # Create the exact same payload the UI sends
        dummy_data = []
        for i in range(100):
            dummy_data.append(0.5)
        
        payload = {
            "model": "resnet18",
            "data": [dummy_data]
        }
        
        print(f"📤 Testing prediction with {len(payload['data'][0])} data points...")
        
        response = requests.post(
            f"{base_url}/predict",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"✅ Prediction: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            predictions = data['predictions'][0]['predictions']
            print(f"   🏆 Top prediction: {predictions[0]['class_name']} ({predictions[0]['confidence']:.3f})")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Prediction: {e}")
    
    print()
    print("🌐 If API tests pass, your UI should work at:")
    print("   http://localhost:3000")
    print()
    print("💡 If you still see HTTP 422 errors:")
    print("   1. Open browser dev tools (F12)")
    print("   2. Check Console tab for detailed errors")
    print("   3. Check Network tab to see the actual request")


if __name__ == "__main__":
    test_api_endpoints()