import sqlite3
import pandas as pd
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    external_id = Column(String(50), nullable=True)  # Associated Plane Issue ID
    created_at = Column(DateTime, default=datetime.utcnow)
    datasets = relationship(
        "Dataset", back_populates="project", cascade="all, delete-orphan"
    )


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    filename = Column(String(255))
    file_type = Column(String(20))  # csv, excel, sqlite
    row_count = Column(Integer)
    col_count = Column(Integer)
    metadata_json = Column(Text)  # JSON string of column names/types
    data_json = Column(Text)  # The actual content of the dataset
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="datasets")


class WarehouseASN(Base):
    """Advanced Shipping Notice - Expected Inventory."""

    __tablename__ = "warehouse_asn"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    asn_number = Column(String(50), unique=True)
    vendor_name = Column(String(100))
    expected_arrival = Column(DateTime)
    status = Column(String(50))  # 'expected', 'received', 'partial'
    items = relationship("ASNItem", back_populates="asn")


class ASNItem(Base):
    __tablename__ = "asn_items"
    id = Column(Integer, primary_key=True)
    asn_id = Column(Integer, ForeignKey("warehouse_asn.id"))
    sku = Column(String(100))
    expected_quantity = Column(Integer)
    received_quantity = Column(Integer, default=0)
    asn = relationship("WarehouseASN", back_populates="items")


class WarehouseReceiving(Base):
    """Actual arrival and unloading at the dock."""

    __tablename__ = "warehouse_receiving"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    asn_id = Column(Integer, ForeignKey("warehouse_asn.id"), nullable=True)
    dock_door = Column(String(20))
    arrival_time = Column(DateTime, default=datetime.utcnow)
    unloading_end_time = Column(DateTime)
    associate_id = Column(String(50))
    total_units_unloaded = Column(Integer)


class WarehouseBinMaster(Base):
    """Static warehouse layout (Building Topology)."""

    __tablename__ = "warehouse_bins"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    bin_id = Column(String(50), unique=True)
    zone = Column(String(20))
    aisle = Column(Integer)
    level_height = Column(String(5))  # A (low) to E (high)
    is_active = Column(Integer, default=1)


class WarehouseStow(Base):
    """The 'Random Stow' transaction into a specific bin."""

    __tablename__ = "warehouse_stows"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    sku = Column(String(100))
    bin_id = Column(String(50), ForeignKey("warehouse_bins.bin_id"))
    quantity = Column(Integer)
    stow_time = Column(DateTime, default=datetime.utcnow)
    associate_id = Column(String(50))
    stow_uph_baseline = Column(Float)


class WarehouseInventory(Base):
    """Snapshot of current inventory state (Bin Map)."""

    __tablename__ = "warehouse_inventory"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    bin_id = Column(String(50))
    sku = Column(String(100))
    quantity = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)
    is_hot_pick = Column(Integer, default=0)  # Optimization flag


class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Resolve relative to this file's directory to ensure it works from any CWD
            db_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../data/dashboards.db")
            )

        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self._ensure_schema_uptodate()

    def _ensure_schema_uptodate(self):
        """Ensures existing tables have all columns defined in the models."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # Migration for datasets
            cursor.execute("PRAGMA table_info(datasets)")
            columns = [info[1] for info in cursor.fetchall()]
            if "data_json" not in columns:
                cursor.execute("ALTER TABLE datasets ADD COLUMN data_json TEXT")

            # Check for projects table (registry for multi-project vault)
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='projects'"
            )
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE TABLE projects (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        external_id TEXT,
                        created_at DATETIME
                    )
                """)
            else:
                # Migration for projects
                cursor.execute("PRAGMA table_info(projects)")
                proj_columns = [info[1] for info in cursor.fetchall()]
                if "external_id" not in proj_columns:
                    cursor.execute("ALTER TABLE projects ADD COLUMN external_id TEXT")

            conn.commit()
        except Exception as e:
            print(f"Migration error: {e}")
        finally:
            conn.close()

    def get_session(self):
        return self.Session()

    def get_all_projects(self):
        """Retrieves all projects from the database."""
        session = self.get_session()
        try:
            return session.query(Project).all()
        finally:
            session.close()


# Global instance for easy access
db_manager = DatabaseManager()
