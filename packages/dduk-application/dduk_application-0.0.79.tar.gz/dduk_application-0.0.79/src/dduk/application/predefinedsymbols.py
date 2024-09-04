#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
from enum import Enum


#--------------------------------------------------------------------------------
# 미리 선언된 내장 심볼 목록.
#--------------------------------------------------------------------------------
class PredefinedSymbols(Enum):
	SYMBOL_SOURCE = "SOURCE" # 소스.
	SYMBOL_BUILD = "BUILD" # 빌드.
	SYMBOL_SERVICE = "SERVICE" # 서비스.
	SYMBOL_LOG = "LOG" # 로그.
	SYMBOL_SUBPROCESS = "SUBPROCESS" # 서브프로세스.
