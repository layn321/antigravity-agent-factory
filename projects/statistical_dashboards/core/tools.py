import json
from langchain_core.tools import tool
from core.database import db_manager
from core.data_manager import DataManager

dm = DataManager()


@tool
def get_dataset_metadata(dataset_id: int) -> str:
    """Retrieves metadata and column information for a specific dataset ID."""
    from core.database import Dataset

    session = db_manager.get_session()
    ds = session.query(Dataset).filter_by(id=dataset_id).first()
    if not ds:
        session.close()
        return f"Dataset {dataset_id} not found."
    meta = json.loads(ds.metadata_json)
    session.close()
    return json.dumps(meta, indent=2)


@tool
def get_dataset_summary(dataset_id: int) -> str:
    """Retrieves summary statistics for a dataset."""
    df = dm.get_dataset_data(dataset_id, db_manager)
    if df is None:
        return f"Failed to load data for dataset {dataset_id}."

    stats = dm.get_summary_stats(df)
    # Second pass of sanitization for absolute JSON safety
    import os

    return json.dumps(
        stats,
        indent=2,
        default=lambda x: None
        if isinstance(x, float) and (os.math.isnan(x) or os.math.isinf(x))
        else str(x),
    )


DATA_TOOLS = [get_dataset_metadata, get_dataset_summary]
