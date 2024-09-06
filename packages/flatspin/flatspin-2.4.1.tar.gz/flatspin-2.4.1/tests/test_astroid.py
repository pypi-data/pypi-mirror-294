import numpy as np
from numpy.linalg import norm
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal
import matplotlib.pyplot as plt

from flatspin.astroid import gsw, gsw_implicit, gsw_astroid, astroid_params

def sw_analytical(hc, phi):
    # Analytical solution for classical Stoner-Wohlfarth
    Hs = hc / (np.sin(phi)**(2/3) + np.cos(phi)**(2/3))**(3/2)
    return np.column_stack([Hs * np.cos(phi), Hs * np.sin(phi)])

@pytest.mark.parametrize("hc", [ .1, .2, 1 ])
def test_gsw(hc):
    # Classical Stoner-Wohlfarth
    sw = dict(b=1, c=1, beta=3, gamma=3, hc=hc)

    phi = np.linspace(0, np.pi/2, 11)
    sw_par, sw_perp = sw_analytical(hc, phi).T
    assert_allclose(gsw(sw_par, **sw), sw_perp)

    # Generalized Stoner-Wohlfarth
    #
    # b < 1: GSW astroid should be below SW, except at 90 deg
    b = .5
    c = 1
    params = dict(b=b, c=c, beta=3, gamma=3, hc=hc)

    h_par = b * hc * np.cos(phi)
    h_perp = gsw(h_par, **params)
    sw_perp = gsw(h_par, **sw)

    assert h_perp[-1] == approx(sw_perp[-1])
    assert np.all(h_perp[:-1] < sw_perp[:-1])

    # c < 1: GSW astroid should be below SW, except at 0 deg
    b = 1 
    c = .8
    params = dict(b=b, c=c, beta=3, gamma=3, hc=hc)

    h_par = b * hc * np.cos(phi)
    h_perp = gsw(h_par, **params)
    sw_perp = gsw(h_par, **sw)

    assert h_perp[-1] == approx(c * hc)
    assert h_perp[0] == approx(sw_perp[0])
    assert np.all(h_perp[1:] < sw_perp[1:])

    # b < 1 and c < 1: GSW astroid should be below SW everywhere
    b = .41
    c = .92
    params = dict(b=b, c=c, beta=3, gamma=3, hc=hc)

    h_par = b * hc * np.cos(phi)
    h_perp = gsw(h_par, **params)
    sw_perp = gsw(h_par, **sw)

    assert h_perp[-1] == approx(c * hc)
    assert np.all(h_perp < sw_perp)

    # Curvature: beta and gamma < 3
    # GSW astroid should be above SW everywhere, except at 0 and 90
    b = c = 1
    params = dict(b=b, c=c, beta=2.8, gamma=2.5, hc=hc)

    h_par = b * hc * np.cos(phi)
    h_perp = gsw(h_par, **params)
    sw_perp = gsw(h_par, **sw)

    # plt.plot(sw_par, sw_perp, 'g.-')
    # plt.plot(h_par, h_perp, 'r.-')
    # plt.show()

    assert h_perp[0] == approx(sw_perp[0])
    assert h_perp[-1] == approx(sw_perp[-1])
    assert np.all(h_perp[1:-1] > sw_perp[1:-1])

    # Curvature: beta and gamma > 3
    # GSW astroid should be below SW everywhere, except at 0 and 90
    b = c = 1
    params = dict(b=b, c=c, beta=3.3, gamma=4.5, hc=hc)

    h_par = b * hc * np.cos(phi)
    h_perp = gsw(h_par, **params)
    sw_perp = gsw(h_par, **sw)

    assert h_perp[0] == approx(sw_perp[0])
    assert h_perp[-1] == approx(sw_perp[-1])
    assert np.all(h_perp[1:-1] < sw_perp[1:-1])

@pytest.mark.parametrize("hc", [ .4, 1, 1.3 ])
def test_gsw_astroid(hc):
    # Classical Stoner-Wohlfarth
    kwargs = dict(b=1, c=1, beta=3, gamma=3, hc=hc)

    # 1st quadrant
    angle_range = (0, np.pi/2)
    astroid = gsw_astroid(angle_range=angle_range, **kwargs)
    assert_allclose(astroid[0], [hc, 0])
    assert_allclose(astroid[-1], [0, hc])

    # 2nd quadrant
    angle_range = (np.pi/2, np.pi)
    astroid = gsw_astroid(angle_range=angle_range, **kwargs)
    assert_allclose(astroid[0], [0, hc])
    assert_allclose(astroid[-1], [-hc, 0])

    # 3d quadrant
    angle_range = (np.pi, 3*np.pi/2)
    astroid = gsw_astroid(angle_range=angle_range, **kwargs)
    assert_allclose(astroid[0], [-hc, 0])
    assert_allclose(astroid[-1], [0, -hc])

    # 4th quadrant
    angle_range = (3*np.pi/2, 2*np.pi)
    astroid = gsw_astroid(angle_range=angle_range, **kwargs)
    assert_allclose(astroid[0], [0, -hc])
    assert_allclose(astroid[-1], [hc, 0])

    # Generalized Stoner-Wohlfarth
    # Check that h_par never exceeds b * hc 
    b = .78
    kwargs = dict(b=b, c=1, beta=3, gamma=3, hc=hc)
    angle_range = (0, 2*np.pi)
    astroid = gsw_astroid(angle_range=angle_range, **kwargs)
    h_par, h_perp = astroid.T
    assert np.min(h_par) == -b * hc
    assert np.max(h_par) == b * hc

    # Test rotation: 1st -> 2nd quadrant
    kwargs = dict(b=1, c=1, beta=3, gamma=3, hc=hc, rotation=90)
    angle_range = (0, np.pi/2)
    astroid = gsw_astroid(angle_range=angle_range, **kwargs)
    assert_allclose(astroid[0], [0, hc])
    assert_allclose(astroid[-1], [-hc, 0])

@pytest.mark.parametrize("hc", [ .1, .2, .3 ])
def test_gsw_implicit(hc):
    # Classical Stoner-Wohlfarth
    sw = dict(b=1, c=1, beta=3, gamma=3, hc=hc)

    phi = np.linspace(0, np.pi/2, 11)
    sw_par, sw_perp = sw_analytical(hc, phi).T
    assert_allclose(gsw_implicit(sw_par, sw_perp, **sw), 0)

    # Generalized Stoner-Wohlfarth
    params = dict(b=.5, c=.9, beta=1.8, gamma=7, hc=hc)
    astroid = gsw_astroid(**params)
    h_par, h_perp = astroid.T
    assert_allclose(gsw_implicit(h_par, h_perp, **params), 0)

def test_astroid_params():
    params = astroid_params(shape='ellipse', width=220, height=80, thickness=20)

    assert list(params.keys()) == ['hc', 'sw_b', 'sw_c', 'sw_beta', 'sw_gamma']

    assert params['hc'] == approx(0.151672)
    assert params['sw_b'] == 1.0
    assert params['sw_c'] == approx(1.1)
    assert params['sw_beta'] == approx(2.2)
    assert params['sw_gamma'] == approx(3.3)
