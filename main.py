from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, StreamingResponse
from data_generator import generate_synthetic_data
import pandas as pd
from io import StringIO
import logging

# Initialize FastAPI
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed domains for dataset generation
ALLOWED_DOMAINS = ["healthcare", "finance", "retail", "cybersecurity", "ecommerce", "hr"]

@app.get("/generate_data/{domain}")
def generate_data(
    domain: str,
    rows: int = Query(10, description="Number of rows"),
    missing_values: float = Query(0.0, ge=0.0, le=0.5, description="Fraction of missing values (0-0.5)"),
    add_outliers: bool = Query(False, description="Include outliers in data"),
    output_format: str = Query("json", description="Output format: json or csv")
):
    """Generate synthetic data for a given domain with optional customization."""
    domain = domain.lower()
    

    if domain not in ALLOWED_DOMAINS:
        return JSONResponse(
            content={"error": f"Invalid domain. Choose from: {', '.join(ALLOWED_DOMAINS)}"},
            status_code=400
        )

    logger.info(f"Generating {rows} rows of {domain} data (missing: {missing_values}, outliers: {add_outliers})")

    data = generate_synthetic_data(domain, rows, missing_values, add_outliers)

    if output_format == "csv":
        output = StringIO()
        data.to_csv(output, index=False)
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={domain}_synthetic_data.csv"})

    return {"synthetic_data": data.to_dict(orient="records")}

