from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from get import get_share_list, add_to_db, get_full_history
from models import Stock, PriceHistory, TrackedShares

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(engine)


def UpdateStockList(engine=engine, Session=Session, Stock=Stock):
    session = Session()
    session.query(Stock).delete()
    shares = get_share_list()
    add_to_db(shares, session)


def TrackNew(symbol, TrackedShares=TrackedShares, engine=engine, Session=Session, Stock=Stock):
    session = Session()
    symbol = symbol.upper()
    a = session.query(TrackedShares).filter(TrackedShares.symbol == symbol.upper()).all()
    b = session.query(Stock).filter(Stock.symbol == symbol.upper()).all()
    if len(b) == 1:
        if len(a) < 1:
            share = TrackedShares(symbol=symbol.upper())
            session.add(share)
            session.commit()
            session.close()
        else:
            print(f"{symbol} Already being Tracked")
    else:
        print(f"{symbol} not recognised")


def UpdateStockHistory(TrackedShares=TrackedShares, engine=engine, Session=Session, PriceHistory=PriceHistory):
    session = Session()
    session.query(PriceHistory).delete()
    tracked = session.query(TrackedShares.symbol).all()
    # print(tracked)
    for share in tracked:
        obj = get_full_history(share.symbol)
        session.add_all(obj)
    session.commit()
    session.close()


UpdateStockList()
TrackNew("Infy")
TrackNew("AcC")
TrackNew("3MINDIA")
TrackNew("AKSHAY")
UpdateStockHistory()
