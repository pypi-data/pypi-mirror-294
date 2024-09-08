"""
Testing ZCB for all models.
"""

import pytest
from pytest import approx

from finmc.calc.bond import zcb_price_mc
from finmc.utils.assets import Discounter
from tests.hullwhite.dataset import data_hwmc
from tests.localvol.dataset import data_lvmc


@pytest.fixture(
    params=[
        data_lvmc,
        data_hwmc,
    ]
)
def data(request):
    return request.param()


@pytest.mark.parametrize("maturity", [0.1, 1.0, 3.0, 10.0])
def test_zcb(data, maturity):
    """Test the price of a zero coupon bond."""

    model_cls, dataset, _ = data
    model = model_cls(dataset)

    # Simulated Price of ZCB
    price = zcb_price_mc(
        maturity=maturity,
        asset_name="USD",
        model=model,
    )

    # Get closed form price
    discounter = Discounter(dataset["ASSETS"][dataset["BASE"]])
    expected_price = discounter.discount(maturity)

    error = price - expected_price
    contract = f"ZCB {maturity:4.2f}"
    assert error == approx(0.0, abs=1e-3)

    print(f"{contract}: {price:11.6f} {expected_price:11.6f} {error:9.6f}")
