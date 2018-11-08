#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional


@dataclass
class UIReturn:
    action: Optional[int] = None
    message: Optional[str] = None
