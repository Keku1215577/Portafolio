from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from processor import process_records


app = FastAPI(
    title="Portfolio DataOps API",
    version="1.0.0",
    description="Python API used by n8n to validate and transform sales data.",
)


class ProcessRequest(BaseModel):
    records: list[dict[str, Any]] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/process")
def process(request: ProcessRequest) -> dict[str, Any]:
    try:
        return process_records(request.records)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
