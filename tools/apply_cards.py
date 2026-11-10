#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 .cards 纯文本题卡写进 content/，用法见 cards_io.py 文件头。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cards_io import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
