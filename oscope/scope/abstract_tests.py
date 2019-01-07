import datetime

import pytest

import oscope.scope.abstract as abs_scope

class BlockedScopeImpl(abs_scope.AbstractOscilloscope):
    def is_ready(self) -> bool:
        return False

class UnblockedScopeImpl(abs_scope.AbstractOscilloscope):
    def is_ready(self) -> bool:
        return True

def test_block_ready():
    second = datetime.timedelta(seconds=1)
    with pytest.raises(TimeoutError):
        BlockedScopeImpl().block_on_ready(second)

def test_block_not_ready():
    short = datetime.timedelta(seconds=0.1)
    UnblockedScopeImpl().block_on_ready(short)

def test_get_name():
    assert BlockedScopeImpl().get_name() == "BlockedScopeImpl"
    assert BlockedScopeImpl(name="FooScope").get_name() == "FooScope"
