from __future__ import annotations

from typing import Any

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "product",
    "quantity",
    "unit_price",
    "cost",
    "discount_pct",
]


def _reject(reason: str, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "reason": reason,
        "row": row,
    }


def process_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(records, list):
        raise TypeError("records must be a list")

    if not records:
        return {
            "status": "completed",
            "received": 0,
            "accepted": 0,
            "rejected": 0,
            "revenue": 0.0,
            "gross_profit": 0.0,
            "gross_margin_pct": 0.0,
            "accepted_rows": [],
            "rejected_rows": [],
        }

    frame = pd.DataFrame(records)
    rejected_rows: list[dict[str, Any]] = []

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    frame = frame[REQUIRED_COLUMNS].copy()

    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["product"] = frame["product"].astype("string").str.strip()
    frame["quantity"] = pd.to_numeric(frame["quantity"], errors="coerce")
    frame["unit_price"] = pd.to_numeric(frame["unit_price"], errors="coerce")
    frame["cost"] = pd.to_numeric(frame["cost"], errors="coerce")
    frame["discount_pct"] = pd.to_numeric(frame["discount_pct"], errors="coerce")

    valid_mask = pd.Series(True, index=frame.index)

    for index, row in frame.iterrows():
        original = records[index]

        if pd.isna(row["date"]):
            rejected_rows.append(_reject("invalid_date", original))
            valid_mask.loc[index] = False
            continue

        if pd.isna(row["product"]) or not str(row["product"]).strip():
            rejected_rows.append(_reject("empty_product", original))
            valid_mask.loc[index] = False
            continue

        if pd.isna(row["quantity"]) or row["quantity"] <= 0 or row["quantity"] % 1 != 0:
            rejected_rows.append(_reject("invalid_quantity", original))
            valid_mask.loc[index] = False
            continue

        if pd.isna(row["unit_price"]) or row["unit_price"] < 0:
            rejected_rows.append(_reject("invalid_unit_price", original))
            valid_mask.loc[index] = False
            continue

        if pd.isna(row["cost"]) or row["cost"] < 0 or row["cost"] > row["unit_price"]:
            rejected_rows.append(_reject("invalid_cost", original))
            valid_mask.loc[index] = False
            continue

        if pd.isna(row["discount_pct"]) or not 0 <= row["discount_pct"] <= 100:
            rejected_rows.append(_reject("invalid_discount", original))
            valid_mask.loc[index] = False
            continue

    clean = frame.loc[valid_mask].copy()

    if clean.empty:
        return {
            "status": "completed_with_rejections",
            "received": len(records),
            "accepted": 0,
            "rejected": len(rejected_rows),
            "revenue": 0.0,
            "gross_profit": 0.0,
            "gross_margin_pct": 0.0,
            "accepted_rows": [],
            "rejected_rows": rejected_rows,
        }

    clean["date"] = clean["date"].dt.strftime("%Y-%m-%d")
    clean["quantity"] = clean["quantity"].astype(int)
    clean["discount_pct"] = clean["discount_pct"].round(2)

    clean["revenue"] = (
        clean["quantity"]
        * clean["unit_price"]
        * (1 - clean["discount_pct"] / 100)
    )

    clean["gross_profit"] = clean["revenue"] - (
        clean["quantity"] * clean["cost"]
    )

    revenue = round(float(clean["revenue"].sum()), 2)
    gross_profit = round(float(clean["gross_profit"].sum()), 2)
    margin = round((gross_profit / revenue) * 100, 2) if revenue else 0.0

    accepted_rows = clean.to_dict(orient="records")

    for row in accepted_rows:
        row["unit_price"] = round(float(row["unit_price"]), 2)
        row["cost"] = round(float(row["cost"]), 2)
        row["revenue"] = round(float(row["revenue"]), 2)
        row["gross_profit"] = round(float(row["gross_profit"]), 2)

    return {
        "status": "completed_with_rejections" if rejected_rows else "completed",
        "received": len(records),
        "accepted": len(accepted_rows),
        "rejected": len(rejected_rows),
        "revenue": revenue,
        "gross_profit": gross_profit,
        "gross_margin_pct": margin,
        "accepted_rows": accepted_rows,
        "rejected_rows": rejected_rows,
    }
