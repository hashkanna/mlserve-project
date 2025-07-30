# MLServe Project

A clean, production-ready ML model serving platform built with **Ray Serve** and **FastAPI** for scalable, distributed model inference.

## Features

- **🚀 Ray Serve Only**: Clean implementation focused purely on Ray Serve (no TorchServe)
- **⚡ Fast Inference**: Direct Hugging Face model loading with ~35ms response times
- **📈 Auto-scaling**: 1-3 replicas based on load with intelligent scaling policies
- **🎛️ Model Registry**: Dynamic multi-model management and discovery
- **🖥️ Interactive Web UI**: Professional dashboard for demos and monitoring
- **📊 Real-time Monitoring**: Built-in metrics, logging, and Ray Dashboard
- **🔧 Production Ready**: Health checks, graceful shutdown, and comprehensive error handling

## Architecture

```
┌─────────────────┐     ┌──────────────────┐
│   FastAPI App   │────▶│   Ray Serve      │
│   (Port 8000)   │     │   Deployments    │
└─────────────────┘     └──────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────────┐
│  /api/predict   │     │  ResNet Model    │
│  /api/models    │     │  (Autoscaling)   │
│  /api/ray/status│     └──────────────────┘
└─────────────────┘              │
                                 ▼
                        ┌──────────────────┐
                        │ Model Registry   │
                        │ (Multi-model)    │
                        └──────────────────┘
```

## Project Structure

```
mlserve-project/
├── src/                    # Source code
│   ├── api/               # FastAPI application
│   │   ├── main.py       # App with Ray Serve lifecycle
│   │   └── endpoints/    # API endpoints
│   ├── models/           # Model definitions
│   ├── services/         # Serving backends
│   │   └── ray_serve.py  # Ray Serve integration
│   └── config/           # Configuration
│       └── ray_config.py # Ray Serve configurations
├── tests/                # Test suite
├── ui/                   # Web UI dashboard
├── demo_interview.py     # Interview demo script
├── test_ray_serve.py     # Ray Serve integration tests
├── start_demo.sh         # One-click demo launcher
├── stop_demo.sh          # Demo shutdown script
├── serve_ui.py           # UI server launcher
└── main.py               # Application entry point
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -e .
```

## Quick Start

### 🚀 One-Click Demo (Recommended for Interviews)

```bash
./start_demo.sh
```

This launches everything you need:
- MLServe API with Ray Serve (port 8000)
- Interactive Web UI (port 3000)
- Ray Dashboard (port 8265)
- Opens browser automatically

**Stop all services:**
```bash
./stop_demo.sh
```

### 🎯 Interview Demo Flow

1. **Start the demo:**
   ```bash
   ./start_demo.sh
   ```

2. **Show the Web UI** (http://localhost:3000):
   - Image classification with drag & drop
   - Real-time predictions with confidence scores
   - Load testing with visual metrics
   - System status monitoring

3. **Demonstrate autoscaling:**
   - Click "Heavy Load (20 req)" in the UI
   - Watch Ray Dashboard show replica scaling
   - Show response time distribution

4. **Command-line demo:**
   ```bash
   python demo_interview.py
   ```

### 🔧 Manual Setup

1. Start the MLServe application:
```bash
python main.py
```

2. (Optional) Start the Web UI:
```bash
python serve_ui.py
```

This will:
- Initialize Ray cluster
- Start Ray Serve with autoscaling
- Deploy ResNet-18 model
- Launch FastAPI on port 8000
- Open Ray Dashboard on port 8265

3. Check service status:
```bash
# API health check
curl http://localhost:8000/api/v1/health

# Ray Serve status
curl http://localhost:8000/api/v1/ray/status

# List available models
curl http://localhost:8000/api/v1/models
```

4. Make predictions:
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "resnet18",
    "data": [[0.5, 0.6, 0.7]]  # Sample RGB pixel values (normalized 0-1)
  }'
```

## Ray Serve Features

### Autoscaling
The ResNet model deployment automatically scales between 1-3 replicas based on load:
```python
autoscaling_config={
    "min_replicas": 1,
    "max_replicas": 3,
    "target_num_ongoing_requests_per_replica": 10,
}
```

### Model Registry
The integrated model registry allows dynamic model management:
- Register new models at runtime
- List all available models
- Route requests to specific models
- Track model versions and status

### Monitoring
- **Ray Dashboard**: http://localhost:8265
  - View cluster resources
  - Monitor deployment replicas
  - Track request metrics
  - Debug performance issues

### Health Checks
- Deployment health checks every 10 seconds
- Graceful shutdown with 20-second timeout
- Automatic replica restart on failure

## Web UI Dashboard

The MLServe Web UI provides an interactive dashboard perfect for demos and monitoring:

### Features
- **🖼️ Image Classification**: Drag & drop image upload with real-time predictions
- **📊 Load Testing**: Visual load testing with autoscaling demonstration  
- **📈 Performance Metrics**: Real-time charts showing latency and throughput
- **🎛️ System Monitoring**: Live status of API, Ray cluster, and replicas
- **📝 Request Logs**: Real-time logging of all requests and responses

### Screenshots
- **Dashboard Overview**: System status, metrics, and controls
- **Image Classification**: Upload images and see predictions with confidence bars
- **Load Testing**: Generate concurrent requests and watch autoscaling
- **Performance Charts**: Visualize latency and throughput over time

### Access URLs
- **Web UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/v1/docs  
- **Ray Dashboard**: http://localhost:8265

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API info |
| `/api/v1/health` | GET | Health check |
| `/api/v1/models` | GET | List available models |
| `/api/v1/predict` | POST | Run model inference |
| `/api/v1/ray/status` | GET | Ray cluster and serve status |

## Advanced Usage

### Custom Model Deployment
To add a new model:

1. Create a new Ray Serve deployment:
```python
@serve.deployment(
    ray_actor_options={"num_cpus": 2},
    autoscaling_config={...}
)
class MyModel:
    def __init__(self):
        # Load your model
        pass
    
    async def __call__(self, request):
        # Process request
        pass
```

2. Register with the model registry:
```python
await registry_handle.register_model.remote(
    "my_model",
    my_model_handle,
    {"version": "1.0", "status": "ready"}
)
```

### Performance Tuning
Adjust Ray Serve configuration in `src/config/ray_config.py`:
- CPU/GPU allocation per replica
- Autoscaling parameters
- Health check intervals
- Request timeouts

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Linting
ruff check src/ tests/

# Type checking
mypy src/
```

### Testing Ray Serve Integration
```bash
# Test model deployment
curl http://localhost:8000/api/ray/status

# Load test with multiple concurrent requests
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/predict \
    -H "Content-Type: application/json" \
    -d '{"model": "resnet18", "data": [[]]}' &
done
```

## Configuration

### Ray Configuration
Edit `src/config/ray_config.py` for:
- Deployment resources (CPU/GPU)
- Autoscaling policies
- Health check settings
- Logging configuration

### Application Settings
Environment variables in `src/config/settings.py`:
- `APP_NAME`: Application name
- `API_PREFIX`: API route prefix
- `LOG_LEVEL`: Logging level
- `CORS_ORIGINS`: Allowed CORS origins

## Troubleshooting

### Common Issues

1. **Ray initialization fails**
   - Check if Ray is already running: `ray status`
   - Stop existing Ray: `ray stop`
   - Check port conflicts (8265 for dashboard)

2. **Model deployment fails**
   - Check Ray Dashboard for deployment status
   - Verify model files exist
   - Check resource availability (CPU/GPU)

3. **Slow inference**
   - Monitor autoscaling in Ray Dashboard
   - Adjust `target_num_ongoing_requests_per_replica`
   - Increase `max_replicas` for higher load

## Demo Script for Interview

```bash
# 1. Start the application
python main.py

# 2. Show Ray Dashboard
echo "Ray Dashboard: http://localhost:8265"

# 3. Check API health
curl http://localhost:8000/api/health

# 4. List available models
curl http://localhost:8000/api/models

# 5. Check Ray Serve status
curl http://localhost:8000/api/ray/status

# 6. Make a prediction
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "model": "resnet18",
    "data": [[0.5, 0.5, 0.5]]
  }'

# 7. Demonstrate autoscaling with load
echo "Sending 20 concurrent requests to trigger autoscaling..."
for i in {1..20}; do
  curl -X POST http://localhost:8000/api/predict \
    -H "Content-Type: application/json" \
    -d '{"model": "resnet18", "data": [[]]}' &
done

# Check Ray Dashboard to see replicas scaling up
```

## Key Benefits for Production

1. **🎯 Ray Serve Focus**: Pure Ray Serve implementation without TorchServe complexity
2. **⚡ High Performance**: ~35ms inference with direct Hugging Face model loading
3. **📈 Smart Scaling**: Automatic 1-3 replica scaling based on real load patterns
4. **🛡️ Enterprise Ready**: Health checks, graceful shutdown, and comprehensive monitoring
5. **🔧 Developer Friendly**: One-click demo, interactive UI, and clean architecture
6. **💰 Cost Effective**: Efficient resource usage with intelligent scaling policies

## Recent Updates

### ✅ TorchServe Cleanup (Latest)
- **Removed**: All TorchServe dependencies and complexity  
- **Simplified**: Pure Ray Serve implementation with Hugging Face models
- **Improved**: Faster startup, cleaner codebase, and better performance
- **Focus**: Production-ready Ray Serve platform only

## License

[MIT License](LICENSE)