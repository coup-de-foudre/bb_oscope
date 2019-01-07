import datetime

import pytest

import oscope.abstract_scope as abs_scope

class BlockedScopeImpl(abs_scope.AbstractOscilloscope):
    def is_ready(self) -> bool:
        return False

class UnblockedScopeImpl(abs_scope.AbstractOscilloscope):
    def is_ready(self) -> bool:
        return True

def test_block_ready():
    with pytest.raises(TimeoutError):
        BlockedScopeImpl().block_on_ready(datetime.timedelta(seconds=1))

def test_block_not_ready():
    UnblockedScopeImpl().block_on_ready(datetime.timedelta(seconds=0.1))


def test_get_name():
    assert BlockedScopeImpl().get_name() == "BlockedScopeImpl"
    assert BlockedScopeImpl(name="FooScope").get_name() == "FooScope"
