"""
JAXert: JAX assertion
---------------------

JAXert is small and simple library for assertion with JAX.
"""
from __future__ import annotations

import jax
import jax.numpy as jnp


__all__ = [
    "jax_assert",
    "assert_allclose",
]



def jax_assert(cond: bool, msg: string = "", *, debug: bool = True) -> None:
    """
    assert with JAX

    Parameters
    ----------
    cond : bool
        Assertion condition
    msg : string, optional
        Assertion message
    debug : bool, optional
        When ``False``, assertion is disabled.
    """
    if not (__debug__ and debug):
        return

    def assert_callback(c):
        # Although `jax.lax.cond()` executes only single branch,
        # `vmap()` etc. transforms to `jax.lax.select()` which executes both branches,
        # so that we recheck condition again.
        if not c:
            raise AssertionError(msg)

    jax.lax.cond(
        cond,
        lambda: None,
        lambda: jax.debug.callback(assert_callback, cond),
    )


@jax.jit
def _diff(actual: jax.Array, desired: jax.Array) -> tuple[jax.Array, jax.Array]:
    """

    """
    a = jnp.abs(jnp.subtract(actual, desired))
    r = jnp.abs(jnp.divide(a, desired))

    return jnp.max(a), jnp.max(r)


def assert_allclose(actual: jax.Array, desired: jax.Array,
                    rtol: float = 1e-7, atol: float = 0,
                    equal_nan: bool = True, *,
                    debug: bool = True,
                    fast: bool = False) -> None:
    """
    assert all values are close

    Parameters
    ----------
    actual : jax.Array
    desired : jax.Array
    rtol : float, optional
        Relative tolerance. Default is ``1e-7``.
    atol : float, optional
        Absolute tolerance. Default is ``0``.
    equal_nan : bool, optional
        If ``True`` (default), ``NaN`` is considered to equal to ``NaN``.
    debug : bool, optional
        If ``False``, assertion is disabled.
    fast : bool, optional
        If ``False`` (default), show absolute and relative differences on error message.
    """
    if not (__debug__ and debug):
        return

    jax_assert(
        actual.shape == desired.shape,
        f"shape mismatch: {actual.shape} != {desired.shape}",
    )

    a = "NOT CALC"
    r = "NOT CALC"
    if not fast:
        a_num, r_num = _diff(actual, desired)
        a = str(a_num)
        r = str(r_num)

    jax_assert(
        jnp.allclose(actual, desired, rtol=rtol, atol=atol, equal_nan=equal_nan),
        f"not close: abs={a}, rel={r}",
    )
