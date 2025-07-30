#!/usr/bin/env python3
"""Interview demo script for MLServe with Ray Serve."""

import requests
import json
import time


def demo_header():
    """Print demo header."""
    print("=" * 80)
    print("🚀 MLServe with Ray Serve - Interview Demo")
    print("=" * 80)
    print()


def check_service(name, url, expected_status=200):
    """Check if a service is responding."""
    try:
        response = requests.get(url)
        if response.status_code == expected_status:
            print(f"✅ {name}: Service is running")
            return True
        else:
            print(f"❌ {name}: Service returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: Service not available - {e}")
        return False


def demo_api_overview():
    """Demonstrate the API overview."""
    print("📋 API Overview")
    print("-" * 40)
    
    response = requests.get("http://localhost:8000/")
    if response.status_code == 200:
        data = response.json()
        print(f"🔗 Service: {data['message']}")
        print(f"📊 Ray Dashboard: {data['ray_dashboard']}")
        print(f"📖 API Docs: http://localhost:8000{data['docs']}")
        print()
        print("Available Endpoints:")
        for name, endpoint in data['endpoints'].items():
            print(f"  • {name}: {endpoint}")
    print()


def demo_model_registry():
    """Demonstrate the model registry."""
    print("🤖 Model Registry")
    print("-" * 40)
    
    response = requests.get("http://localhost:8000/api/v1/models")
    if response.status_code == 200:
        models = response.json()['models']
        for model in models:
            print(f"📦 Model: {model['name']}")
            print(f"   Version: {model['version']}")
            print(f"   Status: {model['status']}")
            print(f"   Framework: {model['framework']}")
            print(f"   Input Shape: {model['input_shape']}")
    print()


def demo_ray_cluster():
    """Demonstrate Ray cluster status."""
    print("⚡ Ray Cluster Status")
    print("-" * 40)
    
    response = requests.get("http://localhost:8000/api/v1/ray/status")
    if response.status_code == 200:
        status = response.json()
        print(f"🎯 Ray Status: {status['status']}")
        
        resources = status['resources']
        print(f"💻 Total CPUs: {resources['total']['CPU']}")
        print(f"📊 Available CPUs: {resources['available']['CPU']}")
        print(f"💾 Memory: {resources['total']['memory'] / 1e9:.1f}GB")
        
        print(f"🌐 Dashboard: http://localhost:8265")
    print()


def demo_inference():
    """Demonstrate model inference."""
    print("🔮 Model Inference Demo")
    print("-" * 40)
    
    # Sample prediction request
    payload = {
        "model": "resnet18",
        "data": [[0.5] * 100]  # Dummy image data
    }
    
    print("📤 Sending prediction request...")
    start_time = time.time()
    
    response = requests.post(
        "http://localhost:8000/api/v1/predict",
        json=payload
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    if response.status_code == 200:
        result = response.json()
        predictions = result['predictions'][0]['predictions']
        
        print(f"⚡ Inference completed in {duration:.3f}s")
        print("🏆 Top predictions:")
        
        for i, pred in enumerate(predictions[:3], 1):
            confidence = pred['confidence'] * 100
            print(f"   {i}. {pred['class_name']}: {confidence:.1f}%")
    else:
        print(f"❌ Prediction failed: {response.status_code}")
    print()


def demo_autoscaling():
    """Demonstrate autoscaling with concurrent requests."""
    print("📈 Autoscaling Demo")
    print("-" * 40)
    print("Sending 15 concurrent requests to trigger autoscaling...")
    print("Watch the Ray Dashboard to see replicas scale up!")
    print()
    
    import concurrent.futures
    
    def make_request(request_id):
        payload = {"model": "resnet18", "data": [[0.5] * 100]}
        start = time.time()
        response = requests.post("http://localhost:8000/api/v1/predict", json=payload)
        duration = time.time() - start
        return request_id, response.status_code, duration
    
    # Send concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(make_request, i) for i in range(15)]
        
        successful = 0
        total_time = 0
        
        for future in concurrent.futures.as_completed(futures):
            req_id, status, duration = future.result()
            if status == 200:
                successful += 1
            total_time += duration
            print(f"   Request {req_id:2d}: {status} ({duration:.3f}s)")
    
    avg_time = total_time / len(futures)
    print(f"\n📊 Results: {successful}/15 successful")
    print(f"⏱️  Average response time: {avg_time:.3f}s")
    print("🎯 Check Ray Dashboard to see if replicas scaled up!")
    print()


def demo_monitoring():
    """Show monitoring capabilities."""
    print("📊 Monitoring & Observability")
    print("-" * 40)
    print("🌐 Ray Dashboard: http://localhost:8265")
    print("   • View cluster resources and utilization")
    print("   • Monitor deployment replicas and scaling")
    print("   • Track request metrics and performance")
    print("   • Debug and troubleshoot issues")
    print()
    print("📖 API Documentation: http://localhost:8000/api/v1/docs")
    print("   • Interactive Swagger UI")
    print("   • Test endpoints directly")
    print("   • View request/response schemas")
    print()


def main():
    """Run the complete demo."""
    demo_header()
    
    # Check services
    print("🔍 Service Health Check")
    print("-" * 40)
    services = [
        ("FastAPI", "http://localhost:8000/api/v1/health"),
        ("Ray Dashboard", "http://localhost:8265"),
    ]
    
    all_healthy = True
    for name, url in services:
        if not check_service(name, url):
            all_healthy = False
    
    if not all_healthy:
        print("\n❌ Some services are not running. Please start the application first:")
        print("   python main.py")
        return
    
    print()
    
    # Demo sections
    demo_api_overview()
    demo_model_registry()
    demo_ray_cluster()
    demo_inference()
    demo_autoscaling()
    demo_monitoring()
    
    print("🎉 Demo Complete!")
    print("=" * 80)
    print("Key Features Demonstrated:")
    print("  ✅ Ray Serve integration with autoscaling")
    print("  ✅ FastAPI REST endpoints")
    print("  ✅ Model registry and management")
    print("  ✅ Real-time inference with ResNet-18")
    print("  ✅ Distributed scaling under load")
    print("  ✅ Monitoring and observability")
    print("=" * 80)


if __name__ == "__main__":
    main()