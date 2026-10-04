# Architecture

## Responsibility boundaries

### n8n

n8n is responsible for:

- Receiving the event through a webhook.
- Calling the Python service.
- Routing the result.
- Returning the automation result to the caller.

### Python API

Python is responsible for:

- Validation.
- Normalization.
- Business rules.
- Calculation of revenue and gross profit.
- Construction of accepted and rejected datasets.

## Why separate the components?

Separating orchestration from transformation avoids placing all business logic inside the workflow. The same Python service can later be consumed by another workflow, an application backend or a scheduled process.

## Current flow

```text
POST /webhook/portfolio-data-automation
            |
            v
       n8n Webhook
            |
            v
       HTTP Request
            |
            v
   Python FastAPI /process
            |
            +--> Data validation
            +--> Data normalization
            +--> KPI calculation
            +--> Rejected rows
            |
            v
       n8n response
```

## Future evolution

A production version could add:

- PostgreSQL persistence.
- Scheduled ingestion.
- Authentication and authorization.
- Error notifications.
- Structured logging.
- Monitoring and metrics.
- Retry policies.
- Data lineage.
- Power BI or another BI destination.

## Security considerations

The demo is intended for local development. Credentials and secrets should never be committed to the repository. Webhooks exposed outside a controlled environment should use authentication and appropriate network protections.
