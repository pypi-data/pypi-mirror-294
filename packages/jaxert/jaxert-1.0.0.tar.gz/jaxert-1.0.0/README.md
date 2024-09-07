# JAXert: Assertion with JAX

JAXert provides simple assertions working with
[JAX](https://jax.readthedocs.io/en/latest/index.html).

These assertions are designed for testing.


## Usage
- `jax_assert(cond)`
- `assert_allclose(actual, desired)`


Other options are described their docstrings.


## Internals
To raise errors even in jitted functions,
we utilize `jax.debug.callback`.


JAX has another mechanism
[checkify](https://jax.readthedocs.io/en/latest/debugging/checkify_guide.html),
where errors are converted to an additional return value containing error informations.
The biggest disadvantage is that we have to handle such errors at outside jitted functions,
which means we must change its call signature.


## Known Limitations
- Depending on usages, `AssertionError` or
  `jaxlib.xla_extension.XlaRuntimeError` are raised. We cannot control
  error class consistently.
- Even though catching errors, JAX automatically dumps stack traces,
  which might be annoying.
