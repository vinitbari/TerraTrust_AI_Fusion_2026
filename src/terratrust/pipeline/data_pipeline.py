"""Data ingestion, validation, and feature preparation pipeline for TerraTrust AI."""

from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

from terratrust.contracts.schemas import ClimateRequest, YieldPredictionRequest


class DataPipeline:
    """Agricultural and Climate Data Engineering Pipeline."""

    REQUIRED_YIELD_COLUMNS = ["Fertilizer", "temp", "N", "P", "K"]

    @classmethod
    def validate_yield_features(cls, df: pd.DataFrame) -> tuple[bool, List[str]]:
        """Validate that a tabular dataset satisfies all required schema constraints."""
        missing = [col for col in cls.REQUIRED_YIELD_COLUMNS if col not in df.columns]
        errors = []
        if missing:
            errors.append(f"Missing required columns: {missing}")
            return False, errors

        # Value bounds validation
        if (df["Fertilizer"] < 0).any():
            errors.append("Negative Fertilizer values detected.")
        if (df["temp"] < -20).any() or (df["temp"] > 65).any():
            errors.append("Unrealistic temperature values (< -20C or > 65C) detected.")
        if (df["N"] < 0).any() or (df["P"] < 0).any() or (df["K"] < 0).any():
            errors.append("Negative N/P/K soil nutrient concentrations detected.")

        return len(errors) == 0, errors

    @classmethod
    def create_inference_feature_row(
        cls,
        fertilizer: float,
        temperature: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
    ) -> pd.DataFrame:
        """Construct a validated 1-row DataFrame strictly conforming to the model feature schema."""
        return pd.DataFrame([
            {
                "Fertilizer": float(fertilizer),
                "temp": float(temperature),
                "N": float(nitrogen),
                "P": float(phosphorus),
                "K": float(potassium),
            }
        ])

    @classmethod
    def audit_dataset_file(cls, csv_path: Path) -> Dict[str, Any]:
        """Perform data quality and schema audit on a local CSV dataset file."""
        if not csv_path.exists():
            return {
                "status": "FILE_NOT_FOUND",
                "path": str(csv_path),
                "message": "Dataset file does not exist.",
            }

        df = pd.read_csv(csv_path)
        valid, errors = cls.validate_yield_features(df)
        return {
            "status": "VALID" if valid else "SCHEMA_ERRORS",
            "total_rows": len(df),
            "columns": list(df.columns),
            "missing_values": int(df.isnull().sum().sum()),
            "errors": errors,
            "summary_stats": df.describe().to_dict(),
        }
