# MLServe Project

A production-ready machine learning model serving platform using FastAPI, TorchServe, and Ray Serve.

## Features

- **Multiple Serving Backends**: Support for both TorchServe and Ray Serve
- **RESTful API**: FastAPI-based endpoints for model inference
- **Model Management**: Easy model deployment and versioning
- **Monitoring**: Built-in metrics and logging
- **Scalable**: Horizontal scaling with Ray Serve
- **Explainability**: Captum integration for model interpretability

## Project Structure

```
mlserve-project/
├── src/                    # Source code
│   ├── api/               # FastAPI application
│   ├── models/            # Model definitions
│   ├── services/          # Serving backends
│   └── config/            # Configuration
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── models/                # Model artifacts
├── docker/                # Docker configurations
└── docs/                  # Documentation
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

1. Build a model archive:
```bash
bash scripts/build_resnet.sh
```

2. Start the FastAPI server:
```bash
uvicorn src.api.main:app --reload
```

3. Make predictions:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"model": "resnet18", "data": [...]}'
```

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

## Configuration

Configuration is managed through environment variables and `src/config/settings.py`.

### Environment Variables
- `MODEL_STORE_PATH`: Path to model storage directory
- `TORCHSERVE_PORT`: TorchServe inference port
- `RAY_SERVE_PORT`: Ray Serve port
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

[MIT License](LICENSE)