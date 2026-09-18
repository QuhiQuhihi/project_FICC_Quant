import numpy as np
import QuantLib as ql
import pytest
from research.pricing import (
    DATE,
    fixture,
    curves,
    bond,
    swap,
    valuation_date,
    quote_risk,
    fx_forward,
)


def test_global_date_restored_even_on_error():
    old = ql.Settings.instance().evaluationDate
    with pytest.raises(RuntimeError):
        with valuation_date():
            assert ql.Settings.instance().evaluationDate == DATE
            raise RuntimeError("test")
    assert ql.Settings.instance().evaluationDate == old


def test_known_flat_discount_and_bond():
    with valuation_date():
        d = ql.FlatForward(DATE, 0.04, ql.Actual365Fixed())
        date = DATE + 365
        assert d.discount(date) == pytest.approx(np.exp(-0.04))
        b, cashflows = bond(d)
        assert b.NPV() == pytest.approx(cashflows.pv.sum(), abs=1e-8)
        assert b.cleanPrice() + b.accruedAmount() == pytest.approx(b.dirtyPrice(), abs=1e-10)


def test_calibration_cashflows_and_par_swap():
    with valuation_date():
        d, p, res = curves()
        assert res.residual.abs().max() < 1e-8
        b, bcf = bond(d)
        s, scf, _ = swap(d, p)
        assert b.NPV() == pytest.approx(bcf.pv.sum(), abs=1e-8)
        assert s.NPV() == pytest.approx(scf.pv.sum(), abs=1e-8)
        assert s.NPV() == pytest.approx(0, abs=1e-8)
        assert d.discount(d.maxDate()) > 0
        assert (bcf.accrual > 0).all() and (scf.accrual > 0).all()


def test_quote_bump_convergence_and_hedge():
    with valuation_date():
        q = fixture()
        d, p, _ = curves(q)
        _, _, coupon = swap(d, p)
        risks = [quote_risk(q, coupon, b)[0] for b in [0.1, 1, 5]]
        np.testing.assert_allclose(risks[0], risks[2], atol=1e-4, rtol=0)
        assert risks[1][0] < 0 and risks[1][1] > 0
        hedge = -risks[1][0] / risks[1][1]
        assert risks[1][0] + hedge * risks[1][1] == pytest.approx(0, abs=1e-12)


def test_fx_cashflows_and_negative_rates():
    forward = fx_forward(1.1, 0.96, 0.98)
    assert 1.1 * 0.98 - forward * 0.96 == pytest.approx(0)
    assert 1.1 * 0.98 - (forward + 0.01) * 0.96 < 0
    # Negative rates legitimately produce discount factors above one.
    assert fx_forward(1.0, 1.02, 1.01) == pytest.approx(1.01 / 1.02)
    with pytest.raises(ValueError):
        fx_forward(1.0, 0.0, 0.9)
