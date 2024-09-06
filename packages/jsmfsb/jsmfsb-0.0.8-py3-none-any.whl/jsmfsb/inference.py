# inference.py
# Code relating to Chapters 10 and 11

import jax
import jax.numpy as jnp
from jax import jit


def metropolisHastings(key, init, logLik, rprop,
                       ldprop=lambda n, o: 1, ldprior=lambda x: 1,
                       iters=10000, thin=10, verb=True):
    """Run a Metropolis-Hastings MCMC algorithm for the parameters of a
    Bayesian posterior distribution

    Run a Metropolis-Hastings MCMC algorithm for the parameters of a
    Bayesian posterior distribution. Note that the algorithm carries
    over the old likelihood from the previous iteration, making it
    suitable for problems with expensive likelihoods, and also for
    "exact approximate" pseudo-marginal or particle marginal MH
    algorithms.
    
    Parameters
    ----------
    key: JAX random number key
      A key to seed the simulation.
    init : vector
      A parameter vector with which to initialise the MCMC algorithm.
    logLik : (stochastic) function
      A function which takes two arguments: a JAX random key and
      a parameter (the same type as `init`) as its
      second argument. It should return the log-likelihood of the
      data. Note that it is fine for this to return the log of an
      unbiased estimate of the likelihood, in which case the
      algorithm will be an "exact approximate" pseudo-marginal MH
      algorithm. This is the reason why the function should accept
      a JAX random key. In the "vanilla" case, where the log-likelihood
      is deterministic, the function should simply ignore the key that
      is passed in.
    rprop : stochastic function
      A function which takes a random key and a current parameter
      as its two required arguments and returns a single sample
      from a proposal distribution.
    ldprop : function
      A function which takes a new and old parameter as its first
      two required arguments and returns the log density of the
      new value conditional on the old. Defaults to a flat function which
      causes this term to drop out of the acceptance probability.
      It is fine to use the default for _any_ _symmetric_ proposal,
      since the term will also drop out for any symmetric proposal.
    ldprior : function
      A function which take a parameter as its only required
      argument and returns the log density of the parameter value
      under the prior. Defaults to a flat function which causes this 
      term to drop out of the acceptance probability. People often use 
      a flat prior when they are trying to be "uninformative" or
      "objective", but this is slightly naive. In particular, what
      is "flat" is clearly dependent on the parametrisation of the
      model.
    iters : int
      The number of MCMC iterations required (_after_ thinning).
    thin : int
      The required thinning factor. eg. only store every `thin`
      iterations.
    verb : boolean
      Boolean indicating whether some progress information should
      be printed to the console. Defaults to `True`.

    Returns
    -------
    A matrix with rows representing samples from the posterior
    distribution.

    Examples
    --------
    >>> import jsmfsb
    >>> import jax
    >>> import jax.numpy as jnp
    >>> import jax.scipy as jsp
    >>> k0 = jax.random.key(42)
    >>> k1, k2 = jax.random.split(k0)
    >>> data = jax.random.normal(k1, 250)*2 + 5
    >>> llik = lambda k, x: jnp.sum(jsp.stats.norm.logpdf(data, x[0], x[1]))
    >>> prop = lambda k, x: jax.random.normal(k, 2)*0.1 + x
    >>> jsmfsb.metropolisHastings(k2, jnp.array([1.0,1.0]), llik, prop)
    """
    def step(s, k):
        [x, ll] = s
        k1, k2, k3 = jax.random.split(k, 3)
        prop = rprop(k1, x)
        llprop = logLik(k2, prop)
        a = (llprop - ll + ldprior(prop) -
             ldprior(x) + ldprop(x, prop) - ldprop(prop, x))
        accept = (jnp.log(jax.random.uniform(k3)) < a)
        s = [jnp.where(accept, prop, x), jnp.where(accept, llprop, ll)]
        return s, s
    def itera(s, k):
        if (verb):
            jax.debug.print("{s}", s=s)
        keys = jax.random.split(k, thin)
        _, states = jax.lax.scan(step, s, keys)
        final = [states[0][thin-1], states[1][thin-1]]
        return final, final
    keys = jax.random.split(key, iters)
    _, states = jax.lax.scan(itera, [init, -jnp.inf], keys)
    return states[0]
    

def pfMLLik(n, simX0, t0, stepFun, dataLLik, data, debug=False):
    """Create a function for computing the log of an unbiased estimate of
    marginal likelihood of a time course data set

    Create a function for computing the log of an unbiased estimate of
    marginal likelihood of a time course data set using a simple
    bootstrap particle filter.

    Parameters
    ----------
    n :  int
      An integer representing the number of particles to use in the
      particle filter.
    simX0 : function
      A function with arguments `key`, `t0` and `th`, where ‘t0’ is a time 
      at which to simulate from an initial distribution for the state of the
      particle filter and `th` is a vector of parameters. The return value 
      should be a state vector randomly sampled from the prior distribution.
      The function therefore represents a prior distribution on the initial
      state of the Markov process.
    t0 : float
      The time corresponding to the starting point of the Markov
      process. Can be no bigger than the smallest observation time.
    stepFun : function
      A function for advancing the state of the Markov process, with
      arguments `key`, `x`, `t0`, `deltat` and `th`, with `th` representing a
      vector of parameters.
    dataLLik : function
      A function with arguments `x`, `t`, `y`, `th`,
      where `x` and `t` represent the true state and time of the
      process, `y` is the observed data, and `th` is a parameter vector. 
      The return value should be the log of the likelihood of the observation. The
      function therefore represents the observation model.
    data : matrix
      A matrix with first column an increasing set of times. The remaining
      columns represent the observed values of `y` at those times.

    Returns
    -------
    A function with arguments `key` and `th`, representing a parameter vector, which
    evaluates to the log of the particle filters unbiased estimate of the
    marginal likelihood of the data (for parameter `th`).

    Examples
    --------
    >>> import jax
    >>> import jax.numpy as jnp
    >>> import jax.scipy as jsp
    >>> import jsmfsb
    >>> def obsll(x, t, y, th):
    >>>     return jnp.sum(jsp.stats.norm.logpdf(y-x, scale=10))
    >>> 
    >>> def simX(key, t0, th):
    >>>     k1, k2 = jax.random.split(key)
    >>>     return jnp.array([jax.random.poisson(k1, 50),
    >>>              jax.random.poisson(k2, 100)]).astype(jnp.float32)
    >>> 
    >>> def step(key, x, t, dt, th):
    >>>     sf = jsmfsb.models.lv(th).stepGillespie()
    >>>     return sf(key, x, t, dt)
    >>> 
    >>> mll = jsmfsb.pfMLLik(80, simX, 0, step, obsll, jsmfsb.data.LVnoise10)
    >>> k0 = jax.random.key(42)
    >>> mll(k0, jnp.array([1, 0.005, 0.6]))
    >>> mll(k0, jnp.array([2, 0.005, 0.6]))
    """
    no = data.shape[1]
    times = jnp.concatenate((jnp.array([t0]), data[:,0]))
    deltas = jnp.diff(times)
    obs = data[:,1:no]
    if (debug):
        print(data.shape)
        print(times[range(5)])
        print(deltas[range(5)])
        print(len(deltas))
        print(obs[range(5),:])
    @jit
    def go(key, th):
        key, k1 = jax.random.split(key)
        keys = jax.random.split(k1, n)
        xmat = jax.lax.map(lambda k: simX0(k, t0, th), keys)
        sh = xmat.shape
        if (debug):
            print(sh)
            print(xmat[range(5),:])
        def advance(state, key):
            [i, xmat, ll] = state
            assert(xmat.shape == sh)
            key, k1, k2 = jax.random.split(key, 3)
            keys = jax.random.split(k1, n)
            def prop(k, x):
                return stepFun(k, x, times[i], deltas[i], th)
            propv = jax.vmap(prop)
            xmat = propv(keys, xmat)
            lw = jnp.apply_along_axis(lambda x: dataLLik(
                x, times[i+1], obs[i,], th), 1, xmat)
            m = jnp.max(lw)
            sw = jnp.exp(lw - m)
            ssw = jnp.sum(sw)
            rows = jax.random.choice(k2, n, shape=(n,), p=sw/ssw)
            state = [i+1, xmat[rows,:], ll + m + jnp.log(ssw/n)]
            return state, state
        keys = jax.random.split(key, len(deltas))
        _, states = jax.lax.scan(advance, [0, xmat, 0.0], keys)
        return states[2][len(deltas)]
    return go




# eof

