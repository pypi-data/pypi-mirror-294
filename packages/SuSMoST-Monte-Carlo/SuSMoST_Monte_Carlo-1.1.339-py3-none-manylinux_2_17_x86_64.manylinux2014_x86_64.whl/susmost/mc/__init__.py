from .mc import run, make_metropolis, autocorr_func, make_histo, autocorr_analysis, make_additive_params, group_by_column, group_statistics, stat_digest, wl_setup, wl_analysis
from .metropolis import Metropolis, param_limit

# https://stackoverflow.com/a/56984285/14736976
from pkg_resources import get_distribution, DistributionNotFound
try:
	__version__ = get_distribution(__name__).version
except DistributionNotFound:
	# package is not installed
	pass

__all__ = ['make_metropolis', 'run', 'stat_digest', 'make_additive_params', 'autocorr_func', 'make_histo', 'group_by_column', 'group_statistics', 'autocorr_analysis', 'param_limit', 'wl_setup', 'wl_analysis']
