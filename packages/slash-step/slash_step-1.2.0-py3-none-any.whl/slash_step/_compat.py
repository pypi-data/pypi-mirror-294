import sys

if sys.version_info < (3, 8):
    # pylint: disable=unused-import
    import pkg_resources

    get_distribution = pkg_resources.get_distribution
    PackageNotFoundError = pkg_resources.DistributionNotFound
else:
    # pylint: disable=unused-import
    import importlib.metadata

    get_distribution = importlib.metadata.distribution
    PackageNotFoundError = importlib.metadata.PackageNotFoundError
