from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    title = Column(String)
    studios = Column(String)
    producers = Column(String)
    winner = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Movie(id={self.id}, year={self.year}, title='{self.title}', winner={self.winner})>"

