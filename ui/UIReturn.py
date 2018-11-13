#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class UIReturn:
    action: Optional[int] = None
    message: Optional[str] = None
    id_query: Optional[int] = None
    substitution_ids: Optional[List[int]] = None
