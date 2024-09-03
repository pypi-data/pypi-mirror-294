import uuid
from typing import Dict, List

import pandas as pd
from slugify import slugify


def generate_field_metadata(df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Generate metadata for each column in the given DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        List[Dict[str, str]]: List of dictionaries containing metadata for each column
    """
    metadata = []
    for column in df.columns:
        metadata.append(
            {
                "fld___id": str(uuid.uuid4()),
                "label": column,
                "id": slugify(column, separator="_", regex_pattern=r"[^a-z0-9_]+"),
            }
        )
    return metadata
