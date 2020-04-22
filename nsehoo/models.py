from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Sequence, Float, Date, Integer
from sqlalchemy import create_engine    

engine = create_engine("sqlite:///database.db")
Base = declarative_base()


class Stock(Base):
    __tablename__ = "stock_list"
    symbol = Column(String(20), primary_key=True, nullable=False)
    company_name = Column(String(60), nullable=False)
    series = Column(String(2), nullable=False)
    listed_date = Column(Date, nullable=False)
    paidup_value = Column(Float, nullable=False)
    market_lot = Column(Float, nullable=False)
    isin_number = Column(String(12), nullable=False)
    face_val = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Share(symbol = {self.symbol}," \
               f" Company_name = {self.company_name}," \
               f" listed_date = {self.listed_date})>"


class PriceHistory(Base):
    __tablename__ = "historical_price"
    entry_id = Column(Integer, Sequence("entry_id"), primary_key=True)
    symbol = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    open_val = Column(String, nullable=False)
    high_val = Column(String, nullable=False)
    low_val = Column(String, nullable=False)
    close_val = Column(String, nullable=False)
    adj_val = Column(String, nullable=False)
    volume = Column(String, nullable=False)

    def __repr__(self):
        return f"<PriceHistory(date = {self.date}, open_val = {self.open_val}, close_val = {self.close_val})>"


class TrackedShares(Base):
    __tablename__ = "tracked_shares"
    symbol = Column(String, nullable = False, primary_key=True)

Base.metadata.create_all(engine)