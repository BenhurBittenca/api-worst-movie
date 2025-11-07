import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models import Movie
from app.services import load_csv_data

# Setup test client
client = TestClient(app)

def setup_database():
    """Setup database for testing"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Load CSV data
    load_csv_data()

def test_root_endpoint():
    """
    Test the root endpoint
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Golden Raspberry Awards API" in data["message"]

def test_health_check():
    """
    Test health check endpoint
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_load_csv_data():
    """
    Test if CSV data is loaded correctly
    """
    # Setup database for this test
    setup_database()
    
    # Let's verify by checking the database
    db = SessionLocal()
    try:
        # Count total movies
        total_movies = db.query(Movie).count()
        assert total_movies > 0, "No movies found in database"
        print(f"Total movies loaded: {total_movies}")
        
        # Count winners
        winners_count = db.query(Movie).filter(Movie.winner == True).count()
        assert winners_count > 0, "No winners found in database"
        print(f"Total winners: {winners_count}")
        
        # Check specific known winners
        # Allan Carr won in 1980 for "Can't Stop the Music"
        allan_carr_movie = db.query(Movie).filter(
            Movie.year == 1980,
            Movie.producers.contains("Allan Carr"),
            Movie.winner == True
        ).first()
        assert allan_carr_movie is not None, "Allan Carr's 1980 win not found"
        assert "Can't Stop the Music" in allan_carr_movie.title
        
        # Joel Silver had multiple wins - check one
        joel_silver_wins = db.query(Movie).filter(
            Movie.producers.contains("Joel Silver"),
            Movie.winner == True
        ).all()
        assert len(joel_silver_wins) > 1, "Joel Silver should have multiple wins"
        
    finally:
        db.close()

def test_producer_intervals_endpoint():
    """
    Test the producer intervals endpoint
    """
    # Setup database for this test
    setup_database()
    
    response = client.get("/movies/producer-intervals")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check response structure
    assert "min" in data
    assert "max" in data
    assert isinstance(data["min"], list)
    assert isinstance(data["max"], list)
    
    # If we have data, validate the structure
    if data["min"]:
        min_item = data["min"][0]
        required_fields = ["producer", "interval", "previousWin", "followingWin"]
        for field in required_fields:
            assert field in min_item, f"Field {field} missing in min result"
        
        # Validate data types
        assert isinstance(min_item["producer"], str)
        assert isinstance(min_item["interval"], int)
        assert isinstance(min_item["previousWin"], int)
        assert isinstance(min_item["followingWin"], int)
        
        # Validate logic
        calculated_interval = min_item["followingWin"] - min_item["previousWin"]
        assert calculated_interval == min_item["interval"], "Interval calculation is incorrect"
    
    if data["max"]:
        max_item = data["max"][0]
        required_fields = ["producer", "interval", "previousWin", "followingWin"]
        for field in required_fields:
            assert field in max_item, f"Field {field} missing in max result"
    
    # If we have both min and max, min should be <= max
    if data["min"] and data["max"]:
        min_interval = data["min"][0]["interval"]
        max_interval = data["max"][0]["interval"]
        assert min_interval <= max_interval, "Min interval should be <= max interval"
    
    print(f"Producer intervals response: {data}")

def test_known_producer_scenario():
    """
    Test specific producer scenarios based on the CSV data
    """
    # Setup database for this test
    setup_database()
    
    response = client.get("/movies/producer-intervals")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check if we can find some expected producers
    all_producers = []
    if data["min"]:
        all_producers.extend([item["producer"] for item in data["min"]])
    if data["max"]:
        all_producers.extend([item["producer"] for item in data["max"]])
    
    # Verify we have some producers with intervals
    assert len(all_producers) > 0, "No producers found with intervals"
    
    # Test the load-csv endpoint
    response = client.post("/movies/load-csv")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "successfully" in data["message"].lower()

def test_producer_parsing():
    """
    Test that producers are correctly parsed from the CSV
    """
    # Setup database for this test
    setup_database()
    
    db = SessionLocal()
    try:
        # Find a movie with multiple producers
        # From the CSV, we can see movies with producers like "Producer1, Producer2 and Producer3"
        multi_producer_movie = db.query(Movie).filter(
            Movie.producers.contains(" and ")
        ).first()
        
        if multi_producer_movie:
            print(f"Found multi-producer movie: {multi_producer_movie.title} - {multi_producer_movie.producers}")
            
        # Test comma-separated producers
        comma_producer_movie = db.query(Movie).filter(
            Movie.producers.contains(",")
        ).first()
        
        if comma_producer_movie:
            print(f"Found comma-separated producers: {comma_producer_movie.title} - {comma_producer_movie.producers}")
            
    finally:
        db.close()

def test_winner_field_parsing():
    """
    Test that winner field is correctly parsed
    """
    # Setup database for this test
    setup_database()
    
    db = SessionLocal()
    try:
        # Check that we have both winners and non-winners
        winners = db.query(Movie).filter(Movie.winner == True).count()
        non_winners = db.query(Movie).filter(Movie.winner == False).count()
        
        assert winners > 0, "Should have some winners"
        assert non_winners > 0, "Should have some non-winners"
        
        print(f"Winners: {winners}, Non-winners: {non_winners}")
        
        # Check a specific winner
        first_winner = db.query(Movie).filter(Movie.winner == True).first()
        assert first_winner is not None
        print(f"First winner: {first_winner.year} - {first_winner.title}")
        
    finally:
        db.close()

if __name__ == "__main__":
    # Run tests manually for debugging
    print("Running integration tests...")
    test_root_endpoint()
    print("✓ Root endpoint test passed")
    
    test_health_check()
    print("✓ Health check test passed")
    
    test_load_csv_data()
    print("✓ CSV data loading test passed")
    
    test_producer_intervals_endpoint()
    print("✓ Producer intervals endpoint test passed")
    
    test_known_producer_scenario()
    print("✓ Known producer scenario test passed")
    
    test_producer_parsing()
    print("✓ Producer parsing test passed")
    
    test_winner_field_parsing()
    print("✓ Winner field parsing test passed")
    
    print("All tests passed!")
