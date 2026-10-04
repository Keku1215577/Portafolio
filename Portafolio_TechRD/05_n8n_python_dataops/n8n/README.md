# n8n workflow

## Workflow

`01_sales_data_quality.json`

The workflow exposes a Webhook endpoint:

```text
POST /webhook/portfolio-data-automation
```

Expected payload:

```json
{
  "records": [
    {
      "date": "2026-08-14",
      "product": "Laptop 14",
      "quantity": 2,
      "unit_price": 95000,
      "cost": 73500,
      "discount_pct": 10
    }
  ]
}
```

The workflow forwards the records to the Python API and returns the processing result.

## Import

Import the JSON file from the n8n editor.

After importing, verify that the HTTP Request node points to:

```text
http://python-api:8000/process
```

This hostname works inside the Docker Compose network defined by this project.

## Testing with curl

After activating the workflow:

```bash
curl -X POST http://localhost:5678/webhook/portfolio-data-automation ^
  -H "Content-Type: application/json" ^
  --data "@data/ventas_demo.json"
```

For Linux/macOS, replace `^` with `\`.

## Notes

The exported workflow does not include credentials. For a public repository, credentials should remain managed inside n8n or through environment-specific secret management.
