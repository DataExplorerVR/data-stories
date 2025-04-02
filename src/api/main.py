from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.queries import aggregate_monthly_sinkings
from datetime import datetime
from typing import Optional

app = FastAPI(
    title="Data Stories API",
    description="API for accessing naval sinkings data and visualizations",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Data Stories API"}

@app.get("/api/sinkings/monthly")
async def get_monthly_sinkings(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    try:
        # Get data from database
        df = aggregate_monthly_sinkings(start_date, end_date)
        
        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient='records')
        
        # Format dates for JSON
        for item in data:
            item['sunk_month_year'] = item['sunk_month_year'].strftime('%Y-%m-%d')
        
        return JSONResponse(content={
            "status": "success",
            "data": data
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
