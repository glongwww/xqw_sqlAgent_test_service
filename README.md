# Tianji SQL Test Service

This is a FastAPI service for workflow testing with streaming responses and result logging.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

- **POST /api/v1/workflow/test/stream**: Run a workflow test and stream results.
  - Body: `{"params": {...}, "test_count": 5}`
- **GET /api/v1/workflow/logs**: Get test history logs.
- **GET /api/v1/workflow/logs/{test_id}**: Get details for a specific test.

## Testing

Run the reproduction test script:
```bash
pip install httpx
python repro_test.py
```
