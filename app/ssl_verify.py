from __future__ import annotations

import os
import sys
from typing import Union


def get_verify_option(_: str | None = None) -> Union[str, bool]:
    """
    app 루트(app/) 또는 상위(프로젝트 루트)에 위치한 zscaler_root_ca.cer를 찾아
    존재하면 해당 경로를 반환하고, 없으면 True(시스템 CA) 반환.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    candidates = [
        os.path.join(here, "zscaler_root_ca.cer"),
        os.path.abspath(os.path.join(here, "..", "zscaler_root_ca.cer")),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return True

