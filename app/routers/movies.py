from fastapi import APIRouter, HTTPException
from app.services import get_producer_intervals, load_csv_data

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/producer-intervals")
def get_producer_intervals_endpoint():
    """
    Get producer win intervals (min and max)
    
    Returns the producers with minimum and maximum intervals between consecutive wins
    """
    try:
        result = get_producer_intervals()
        return result
    except Exception as e:
        print(f"Erro no endpoint producer-intervals: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/load-csv")
def load_csv_endpoint():
    """
    Load movie data from CSV file
    
    Clears existing data and loads fresh data from movielist.csv
    """
    try:
        load_csv_data()
        return {"message": "CSV data loaded successfully"}
    except Exception as e:
        print(f"Erro no endpoint load-csv: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading CSV: {str(e)}")

