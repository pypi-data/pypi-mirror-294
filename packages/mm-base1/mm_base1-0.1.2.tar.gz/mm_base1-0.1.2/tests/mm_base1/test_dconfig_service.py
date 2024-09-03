from decimal import Decimal

from mm_base1.models import DConfigType
from mm_base1.services.dconfig_service import DConfigService


def test_get_type():
    assert DConfigService.get_type("a") == DConfigType.STRING
    assert DConfigService.get_type(1) == DConfigType.INTEGER
    assert DConfigService.get_type(1.1) == DConfigType.FLOAT
    assert DConfigService.get_type(Decimal("1.1")) == DConfigType.DECIMAL
    assert DConfigService.get_type(False) == DConfigType.BOOLEAN
