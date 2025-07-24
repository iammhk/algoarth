# database/settings_db.py

from sqlalchemy import create_engine, Column, Integer, String, Boolean, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from utils.logging import get_logger

logger = get_logger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(
    DATABASE_URL,
    pool_size=50,
    max_overflow=100,
    pool_timeout=10
)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    analyze_mode = Column(Boolean, default=False)  # Default to Live Mode
    risk_appetite = Column(String, default='medium')
    zerodha_api_key = Column(String)
    zerodha_api_secret = Column(String)
    goal_short = Column(String)
    goal_medium = Column(String)
    goal_long = Column(String)

def init_db():
    """Initialize the settings database"""
    logger.info("Initializing Settings DB")
    
    # Drop and recreate tables to handle schema changes
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create default settings
    logger.info("Creating default settings (Live Mode)")
    default_settings = Settings(
        analyze_mode=False,
        risk_appetite='medium',
        zerodha_api_key='',
        zerodha_api_secret='',
        goal_short='',
        goal_medium='',
        goal_long=''
    )
    db_session.add(default_settings)
    db_session.commit()

def get_analyze_mode():
    """Get current analyze mode setting"""
    settings = Settings.query.first()
    if not settings:
        settings = Settings(analyze_mode=False)  # Default to Live Mode
        db_session.add(settings)
        db_session.commit()
    return settings.analyze_mode

def set_analyze_mode(mode: bool):
    """Set analyze mode setting"""
    settings = Settings.query.first()
    if not settings:
        settings = Settings(analyze_mode=mode)
        db_session.add(settings)
    else:
        settings.analyze_mode = mode
    db_session.commit()

def get_user_settings():
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db_session.add(settings)
        db_session.commit()
    return settings

def set_user_settings(risk_appetite, zerodha_api_key, zerodha_api_secret, goal_short, goal_medium, goal_long):
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db_session.add(settings)
    settings.risk_appetite = risk_appetite
    settings.zerodha_api_key = zerodha_api_key
    settings.zerodha_api_secret = zerodha_api_secret
    settings.goal_short = goal_short
    settings.goal_medium = goal_medium
    settings.goal_long = goal_long
    db_session.commit()
