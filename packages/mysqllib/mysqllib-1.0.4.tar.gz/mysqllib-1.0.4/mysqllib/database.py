from typing import Optional, Dict, List, Union, Tuple

import mysqllib


class Database:
    def __init__(self):
        self.table = None

    def find(
            self,
            conditions: Dict[str, Union[str, List]] = None,
            columns='*',
            joins: Optional[List[Tuple[str, str, str]]] = None
    ) -> dict:
        return mysqllib.find(table=self.table, conditions=conditions, columns=columns, joins=joins)

    def findall(
            self,
            conditions: Dict[str, Union[str, List]] = None,
            columns='*',
            joins: Optional[List[Tuple[str, str, str]]] = None
    ) -> list:
        return mysqllib.findall(table=self.table, conditions=conditions, columns=columns, joins=joins)

    def update(
            self,
            data: Dict[str, any],
            conditions: Optional[Dict[str, any]] = None
    ) -> bool:
        return mysqllib.update(table=self.table, data=data, conditions=conditions)

    def delete(
            self,
            conditions: Optional[Dict[str, any]] = None
    ) -> bool:
        return mysqllib.delete(table=self.table, conditions=conditions)

    def create(
            self,
            data: Dict[str, any]
    ) -> bool:
        return mysqllib.create(table=self.table, data=data)
