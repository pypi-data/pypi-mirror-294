"""WebtoonScraper의 기본 정보들을 모아놓은 모듈입니다. circular import를 피하기 위해 필요합니다."""

from __future__ import annotations

import logging
import os

from rich.logging import RichHandler

__url__ = "https://github.com/ilotoki0804/WebtoonScraper"
__version_info__ = (4, 1, 0)
__version__ = str.join(".", map(str, __version_info__[:3])) + "".join(map(str, __version_info__[3:]))

_CPU_COUNT = os.cpu_count()
DEFAULT_PROCESS_NUMBER = 1 if _CPU_COUNT is None or _CPU_COUNT < 2 else max(_CPU_COUNT // 2, 10)

logger = logging.getLogger("webtoonscraper_logger")
logger.handlers = [RichHandler(show_time=False, show_path=False)]
logger.setLevel(logging.INFO)
