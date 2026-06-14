import pytest
from decimal import Decimal
from sgqrgen import SgQRGenerator


@pytest.fixture
def qr_gen():
    sgqr_test_str = "00020101021125280009SG.PAYNOW010100211+659876543203011530370254040.005802SG5913TAN AH GAO 63042968"
    return SgQRGenerator(sgqr_test_str)


def test_change_price_happy_path(qr_gen, tmp_path):
    qr_gen.change_price(Decimal("8.00")).change_comment("membership")
    out_file = tmp_path / "output-qrcode.png"
    qr_gen.output_qrcode(str(out_file))
    assert out_file.exists()


@pytest.mark.parametrize("invalid_amount", ["8.00", 8.00])
def test_change_price_type_error(qr_gen, invalid_amount):
    with pytest.raises(TypeError, match="amount must be a Decimal instance"):
        qr_gen.change_price(invalid_amount)


@pytest.mark.parametrize("invalid_decimal", [
    Decimal("8"),
    Decimal("8.0"),
    Decimal("8.000")
])
def test_change_price_value_error(qr_gen, invalid_decimal):
    with pytest.raises(ValueError, match="amount must have exactly 2 decimal places"):
        qr_gen.change_price(invalid_decimal)
