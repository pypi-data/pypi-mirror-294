# tycki

A simple Python tool for MCMC sampling using the amazing [MCMClib](https://github.com/kthohr/mcmc).

## Installation

`tycki` is on PyPI, so just
```
pip install tycki
```

## Usage

`tycki` provides four samples from [MCMClib](https://github.com/kthohr/mcmc):
- Random-walk Metropolis-Hastings `tycki.RWMH`
- Metropolis-adjusted Langevin algorithm `tycki.MALA`
- Hamiltonian Monte Carlo `tycki.HMC`
- No-U-Turn sampler `tycki.NUTS`

For sampling, the algorithms just require a start point, a log density function and - depending on the algorithm -
the gradient of the log density function:

```
import tycki

rwmh = tycki.RWMH()
samples = rwmh.sample(log_density=lambda x: -(x**2).sum(), x0=[0, 0])

mala = tycki.MALA(x0=[0, 0]) # starting point can also be given in constructor
samples = mala.sample(log_density=lambda x: -(x**2).sum(), grad_log_density=lambda x: -2*x)
```

If you're too lazy to derive the gradient of your log density function manually, you can also use
AD tools like `jax`:

```
import tycki
import jax
from jax import grad

@jax.jit
def logp(x, s=1):
        return -.5*(x**2 / s**2).sum()

rwmh = tycki.RWMH(x0=[0, 0])
samples = rwmh.sample(logp, grad(logp))

mala = tycki.MALA(x0=[0, 0])
samples = mala.sample(logp, grad(logp))
```

## Licensing

This project is based on the amazing [MCMClib](https://github.com/kthohr/mcmc) by Keith O'Hara,
licensed under the Apache License 2.0. Modifications and additions in order to make the 
by Richard D. Paul are licensed under MIT License.

See the LICENSE file for the full text of the MIT License.

