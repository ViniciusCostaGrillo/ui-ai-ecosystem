import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    JSON,
    Text,
)
from sqlalchemy.orm import relationship
from backend.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="projects")
    executions = relationship("Execution", back_populates="project", cascade="all, delete-orphan")
    datasets = relationship("Dataset", back_populates="project", cascade="all, delete-orphan")


class Execution(Base):
    __tablename__ = "executions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="pending", index=True)  # pending, running, completed, failed
    config = Column(JSON, nullable=True)  # crawler configs, LLM choices, etc.
    result = Column(JSON, nullable=True)  # generated visual metadata, component code path
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="executions")
    jobs = relationship("Job", back_populates="execution", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="execution", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)  # crawl, analyze, codegen
    status = Column(String(50), nullable=False, default="queued", index=True)  # queued, processing, success, failed
    execution_id = Column(String(36), ForeignKey("executions.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    execution = relationship("Execution", back_populates="jobs")
    logs = relationship("Log", back_populates="job", cascade="all, delete-orphan")


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    execution_id = Column(String(36), ForeignKey("executions.id", ondelete="CASCADE"), nullable=True, index=True)
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=True, index=True)
    level = Column(String(20), nullable=False, default="INFO", index=True)  # DEBUG, INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    execution = relationship("Execution", back_populates="logs")
    job = relationship("Job", back_populates="logs")


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(String(1024), nullable=False)
    screenshot_path = Column(String(1024), nullable=True)
    html_path = Column(String(1024), nullable=True)
    css_path = Column(String(1024), nullable=True)
    markdown_path = Column(String(1024), nullable=True)
    metadata_json = Column(JSON, nullable=True)  # scraped headers, visual structural details
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="datasets")
    crawler_histories = relationship("CrawlerHistory", back_populates="dataset", cascade="all, delete-orphan")


class CrawlerHistory(Base):
    __tablename__ = "crawler_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(1024), nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    dataset = relationship("Dataset", back_populates="crawler_histories")


class TrainingHistory(Base):
    __tablename__ = "training_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name = Column(String(255), nullable=False)
    base_model = Column(String(255), nullable=False)  # e.g., llama-3, qwen-2
    dataset_path = Column(String(1024), nullable=False)
    epochs = Column(Integer, nullable=False, default=1)
    loss = Column(Float, nullable=True)
    status = Column(String(50), nullable=False, default="running", index=True)  # running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
