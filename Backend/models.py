from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, func
from database import Base

class CalculationRecord(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    num1 = Column(Float, nullable=False)
    num2 = Column(Float, nullable=False)
    operation = Column(String(10), nullable=False)
    result = Column(Float, nullable=False)
    
    # server_default relies directly on MySQL's CURRENT_TIMESTAMP
    timestamp = Column(
        DateTime, 
        server_default=func.now(), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )