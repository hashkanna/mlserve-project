#!/usr/bin/env python3
"""Main entry point for MLServe project."""

import uvicorn
from src.api.main import app


def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
