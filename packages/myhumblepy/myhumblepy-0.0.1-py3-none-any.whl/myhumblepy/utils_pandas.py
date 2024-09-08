"""
This module provides helper functions when working with pandas.
"""

import pandas as pd


def fct_collapse(x: pd.Series, mapping_dict: dict) -> pd.Series:
    """
    Collapse a categorical variable into a smaller set of categories.

    Attempt to replicate the fct_collapse function of the forcats R package
    https://forcats.tidyverse.org/reference/fct_collapse.html

    Parameters
    ----------
    x : pd.Series
        The categorical series to be collapsed.
    mapping_dict : dict
        A dictionary where the keys are the new categories and the values are lists
        of existing categories to be collapsed into the new category e.g.
        {"new_class": ["exisiting_class1", "existing_class_2", ...]}

    Returns
    -------
    pd.Series
        The collapsed categorical series.
    """
    return x.replace({val: key for key in mapping_dict for val in mapping_dict[key]})


def fct_relevel(
    x: pd.Series, order: list = None, ordered: bool = False
) -> pd.Categorical:
    """
    Relevel a categorical variable.

    Attempt to replicate the fct_relevel function of the forcats R package


    Parameters
    ----------
    x : pd.Series
        Input categorical variable.
    order : list, optional
        List of categories to be used as the new order. If None, the existing
        order is used. If the length of the list is shorter than the number of
        unique categories in the input, the remaining categories are sorted
        alphabetically and appended to the end of the list.
    ordered : bool, optional
        If True, the output will be an ordered factor.

    Returns
    -------
    pd.Categorical
        Reordered categorical variable.
    """
    if order is None:
        return pd.Categorical(x.astype("category"), ordered=ordered)
    elif len(order) < len(x.dropna().unique()):
        return pd.Categorical(
            x,
            categories=order
            + sorted([e for e in x.dropna().unique() if e not in order]),
            ordered=ordered,
        )
    else:
        return pd.Categorical(x, categories=order, ordered=ordered)
