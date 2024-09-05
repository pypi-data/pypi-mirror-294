from typing import Tuple, List, Dict, Union


def condition_generator(conditions: Dict[str, Union[str, List[Union[str, int]]]]) -> Tuple[str, List[Union[str, int]]]:
    """
    Generates SQL condition clauses and values based on provided conditions.

    Args:
        conditions (Dict[str, Union[str, List[Union[str, int]]]]):
            Dictionary of column conditions where the key is the column name and the value
            is either a simple value (for equality) or a list containing an operator and a value.

    Returns:
        Tuple[List[str], List[Union[str, int]]]:
            A tuple containing a list of SQL condition clauses and a list of corresponding values.
    """
    condition_clauses = []
    values = []

    for column, condition in conditions.items():
        # Check if the condition is a list with operator and value
        if isinstance(condition, list) and len(condition) == 2:
            operator, value = condition
            condition_clauses.append(f"{column} {operator} %s")
            values.append(value)
        else:
            # Simple equality condition
            condition_clauses.append(f"{column} = %s")
            values.append(condition)

    condition_str = " AND ".join(condition_clauses)

    return condition_str, values
