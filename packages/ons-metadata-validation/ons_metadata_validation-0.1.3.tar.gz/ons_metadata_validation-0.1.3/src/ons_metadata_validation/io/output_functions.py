import logging
from itertools import islice
from typing import Dict

import pandas as pd
from openpyxl import Workbook

logger = logging.getLogger()


def ws_to_df(ws) -> pd.DataFrame:
    """convert a single worksheet into a dataframe

    Args:
        ws (Worksheet): openpyxl worksheet

    Returns:
        pd.DataFrame: formatted df
    """
    data = ws.values
    cols = next(data)[1:]
    data = list(data)
    idx = [r[0] for r in data]
    data = (islice(r, 1, None) for r in data)
    df = pd.DataFrame(data, index=idx, columns=cols)
    df = df.iloc[1:]
    return df


def wb_to_df_dict(wb: Workbook) -> Dict[str, pd.DataFrame]:
    """convert a workbook into a dict of dataframes

    Args:
        wb (Workbook): input workbook to convert

    Returns:
        Dict[str, pd.DataFrame]: dict of dataframes with the keys as the tab names
            and the data as dfs
    """
    dfs = {}

    for sheet in wb.sheetnames:
        dfs[sheet] = ws_to_df(wb[sheet])

    return dfs
