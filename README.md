# Data Stories
This is a space where I will include several projects that tell stories from different datasets. Each project uses data analysis and visualization to uncover interesting narratives within the data.

## Project Structure

```
data-stories/
├── data/
│   └── raw/                # Raw data files
├── src/
│   ├── api/               # FastAPI backend service
│   │   ├── main.py        # API endpoints
│   │   └── start_server.sh # Server startup script
│   ├── database/          # Database interaction modules
│   │   └── queries.py     # SQL queries and data retrieval functions
│   └── visualizations/    # Data visualization modules
│       └── monthly_trends.py # Monthly trends visualization
├── .env                   # Environment variables (not in version control)
├── .env.example          # Template for environment variables
└── requirements.txt      # Python dependencies
```

## Database Setup

The project uses MySQL to store and analyze data. The database configuration is managed through environment variables defined in `.env`. To set up the database:

1. Copy `.env.example` to `.env` and fill in your MySQL credentials
2. Install required packages: `pip install -r requirements.txt`
3. The database will be initialized when running queries for the first time

## Queries Module

Located in `src/database/queries.py`, this module provides functions for data analysis:

### Available Functions

- `aggregate_monthly_sinkings(start_date=None, end_date=None)`: 
  - Aggregates naval vessel sinkings by month
  - Returns total count and tonnage
  - Optional date range filtering
  - Returns pandas DataFrame with monthly statistics

## Visualizations

Located in `src/visualizations/`, this directory contains modules for creating data visualizations.

### Monthly Trends (`monthly_trends.py`)

Creates dual-axis line plots showing:
- Number of ships sunk over time
- Total tonnage lost over time

Features:
- Automatic date range handling
- Customizable output paths
- Three preset views:
  1. All-time trends
  2. 1942 specific trends
  3. 1944-1945 trends

## Data Sources

The project currently includes:
- Japanese Naval Sinkings (1941-1945)
  - Location: `data/raw/JAPAN_NAVAL_SINKINGS_RAW_20250401.csv`
  - Contains detailed information about naval vessels sunk during World War II

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your database credentials in `.env`
4. Run queries or create visualizations using the provided modules

Example usage:
```python
# Generate visualizations
python src/visualizations/monthly_trends.py

# Run queries
python src/database/queries.py

# Start API server
cd src/api && uvicorn main:app --reload
```

## API Endpoints

The project includes a FastAPI backend service that exposes the following endpoints:

### GET /api/sinkings/monthly

Returns monthly aggregated data about naval sinkings.

Parameters:
- `start_date` (optional): Filter data from this date (YYYY-MM-DD)
- `end_date` (optional): Filter data to this date (YYYY-MM-DD)

Example response:
```json
{
  "status": "success",
  "data": [
    {
      "sunk_month_year": "1941-12-01",
      "total_sinkings": 24,
      "total_tonnage": 71426.0
    },
    ...
  ]
}
```

## React Integration

To use this API with a React frontend:

1. Start the API server:
   ```bash
   cd src/api
   uvicorn main:app --reload
   ```

2. In your React application:
   ```javascript
   // Example fetch call
   const fetchMonthlyData = async () => {
     try {
       const response = await fetch('http://localhost:8000/api/sinkings/monthly');
       const data = await response.json();
       // Handle the data in your React component
     } catch (error) {
       console.error('Error fetching data:', error);
     }
   };
   ```

3. CORS is already configured to allow requests from `http://localhost:3000` (default React port)

