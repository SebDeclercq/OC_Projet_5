#!/usr/bin/env python3
'''"Container"-like class meant to hold all return
information from the UI to the App'''
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class UIReturn:
    '''"Container"-like class meant to hold all return
    information from the UI to the App'''
    action: Optional[int] = None
    message: Optional[str] = None
    id_query: Optional[int] = None
    substitution_ids: Optional[List[int]] = None
