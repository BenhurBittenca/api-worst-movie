import pandas as pd
import re
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Movie

def load_csv_data():
    """
    Load movie data from CSV file into database
    """
    print("Carregando dados do CSV...")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Movie).delete()
        db.commit()
        print("Dados existentes removidos.")
        
        # Read CSV with semicolon separator
        df = pd.read_csv("movielist.csv", sep=";", encoding='utf-8')
        print(f"CSV lido com {len(df)} registros.")
        
        # Insert data into database
        count = 0
        for _, row in df.iterrows():
            # Convert winner field: "yes" = True, anything else = False
            winner = str(row.get('winner', '')).strip().lower() == 'yes'
            
            movie = Movie(
                year=int(row['year']),
                title=str(row['title']),
                studios=str(row['studios']),
                producers=str(row['producers']),
                winner=winner
            )
            
            db.add(movie)
            count += 1
        
        db.commit()
        print(f"Dados carregados com sucesso! {count} filmes inseridos.")
        
        # Show some stats
        winners_count = db.query(Movie).filter(Movie.winner == True).count()
        print(f"Total de vencedores: {winners_count}")
        
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def get_producer_intervals():
    """
    Calculate producer win intervals for min and max gaps
    """
    print("Calculando intervalos dos produtores...")
    
    db = SessionLocal()
    
    try:
        # Get only winning movies
        winners = db.query(Movie).filter(Movie.winner == True).order_by(Movie.year).all()
        print(f"Encontrados {len(winners)} filmes vencedores.")
        
        # Dictionary to store producer wins: {producer: [years]}
        producer_wins = {}
        
        for movie in winners:
            # Split producers by comma and "and"
            producers_str = movie.producers
            # First split by comma, then by " and "
            producers_list = []
            
            # Split by comma first
            comma_split = producers_str.split(',')
            for part in comma_split:
                # Then split each part by " and "
                and_split = re.split(r'\s+and\s+', part.strip())
                producers_list.extend([p.strip() for p in and_split if p.strip()])
            
            # Add year to each producer
            for producer in producers_list:
                if producer not in producer_wins:
                    producer_wins[producer] = []
                producer_wins[producer].append(movie.year)
        
        print(f"Processados {len(producer_wins)} produtores únicos.")
        
        # Calculate intervals for producers with multiple wins
        producer_intervals = {}
        
        for producer, years in producer_wins.items():
            if len(years) > 1:  # Only producers with multiple wins
                years.sort()  # Ensure years are sorted
                intervals = []
                
                for i in range(len(years) - 1):
                    interval = years[i + 1] - years[i]
                    intervals.append({
                        'interval': interval,
                        'previousWin': years[i],
                        'followingWin': years[i + 1]
                    })
                
                producer_intervals[producer] = intervals
        
        print(f"Encontrados {len(producer_intervals)} produtores com múltiplas vitórias.")
        
        # Find min and max intervals
        all_intervals = []
        for producer, intervals in producer_intervals.items():
            for interval_data in intervals:
                all_intervals.append({
                    'producer': producer,
                    'interval': interval_data['interval'],
                    'previousWin': interval_data['previousWin'],
                    'followingWin': interval_data['followingWin']
                })
        
        if not all_intervals:
            return {"min": [], "max": []}
        
        # Sort by interval to find min and max
        all_intervals.sort(key=lambda x: x['interval'])
        
        min_interval = all_intervals[0]['interval']
        max_interval = all_intervals[-1]['interval']
        
        # Get all producers with min interval
        min_producers = [item for item in all_intervals if item['interval'] == min_interval]
        
        # Get all producers with max interval
        max_producers = [item for item in all_intervals if item['interval'] == max_interval]
        
        print(f"Menor intervalo: {min_interval} anos")
        print(f"Maior intervalo: {max_interval} anos")
        
        return {
            "min": min_producers,
            "max": max_producers
        }
        
    except Exception as e:
        print(f"Erro ao calcular intervalos: {e}")
        raise
    finally:
        db.close()

