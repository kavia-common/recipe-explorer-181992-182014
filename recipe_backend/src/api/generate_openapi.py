import json
import os

from src.api.main import app

"""
Utility script to regenerate the OpenAPI schema based on the current FastAPI app.

This script writes the schema to interfaces/openapi.json which is used by other
containers as the interface contract.
"""

def main():
    # Get the OpenAPI schema
    openapi_schema = app.openapi()

    # Write to file
    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)

if __name__ == "__main__":
    main()
