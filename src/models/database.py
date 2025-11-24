"""Database models for the Research Marketplace."""

from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from uuid import uuid4
import json

from sqlalchemy import create_engine, Column, String, DateTime, Float, Boolean, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class PersonaType(str, Enum):
    CLIMATE = "climate"
    BIOMEDICAL = "bio"
    SOCIAL = "social"
    DATA = "data"


class AccessType(str, Enum):
    AVAILABLE = "available"
    RESTRICTED = "restricted"


class UserRole(str, Enum):
    ADMIN = "admin"
    RESEARCHER = "researcher"
    GUEST = "guest"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    institution = Column(String)
    orcid = Column(String)
    role = Column(String, default=UserRole.RESEARCHER.value)
    persona = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    provider = Column(String)
    format = Column(String)
    size = Column(String)
    sample_count = Column(Integer)
    tags = Column(Text)  # JSON string
    access_type = Column(String, default=AccessType.AVAILABLE.value)
    relevance_scores = Column(Text)  # JSON string mapping persona to score
    last_updated = Column(DateTime, default=datetime.utcnow)
    checksum = Column(String)
    quality_score = Column(Float, default=0.0)

    def get_tags(self) -> List[str]:
        return json.loads(self.tags) if self.tags else []

    def set_tags(self, tags: List[str]):
        self.tags = json.dumps(tags)

    def get_relevance_scores(self) -> Dict[str, float]:
        return json.loads(self.relevance_scores) if self.relevance_scores else {}

    def set_relevance_scores(self, scores: Dict[str, float]):
        self.relevance_scores = json.dumps(scores)


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    discipline = Column(String)
    status = Column(String, default="active")
    owner_id = Column(String)
    persona = Column(String)
    selected_datasets = Column(Text)  # JSON string
    collaborators = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    pre_registration_id = Column(String)

    def get_selected_datasets(self) -> List[str]:
        return json.loads(self.selected_datasets) if self.selected_datasets else []

    def set_selected_datasets(self, datasets: List[str]):
        self.selected_datasets = json.dumps(datasets)


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    project_id = Column(String)
    agent_type = Column(String, nullable=False)
    status = Column(String, default="pending")
    input_data = Column(Text)  # JSON string
    output_data = Column(Text)  # JSON string
    recommendations = Column(Text)  # JSON string
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    project_id = Column(String)
    user_id = Column(String)
    action = Column(String, nullable=False)
    details = Column(Text)  # JSON string
    timestamp = Column(DateTime, default=datetime.utcnow)


# Database initialization
def init_db(db_path: str = "data/marketplace.db"):
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
