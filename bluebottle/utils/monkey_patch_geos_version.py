# From https://gist.github.com/jams2/11a60020a1ada897d79fc4c77fb587eb
"""The version regex in django/contrib/gis/geos/libgeos.py fails on
the latest homebrew geos install at time of writing, with message:
  django.contrib.gis.geos.error.GEOSException: Could not parse version info string "3.8.0-CAPI-1.13.1 "

The trailing whitespace is the culprit. Add a r'\s?$' to the end of the pattern.
"""
import re

import django.contrib.gis.geos.libgeos as libgeos

from django.contrib.gis.geos.libgeos import geos_version, GEOSException



version_regex = re.compile(
    r'^(?P<version>(?P<major>\d+)\.(?P<minor>\d+)\.(?P<subminor>\d+))'
    r'((rc(?P<release_candidate>\d+))|dev)?-CAPI-(?P<capi_version>\d+\.\d+\.\d+)( r\d+)?( \w+)?\s?$'
)


# Exact copy of function in django/contrib/gis/geos/libgeos.py on 1.11.x branch
def geos_version_info():
    """
    Returns a dictionary containing the various version metadata parsed from
    the GEOS version string, including the version number, whether the version
    is a release candidate (and what number release candidate), and the C API
    version.
    """
    ver = geos_version().decode()
    m = version_regex.match(ver)
    if not m:
        raise GEOSException('Could not parse version info string "%s"' % ver)
    return {key: m.group(key) for key in (
        'version', 'release_candidate', 'capi_version', 'major', 'minor', 'subminor')}


# version_regex exists on the 1.11.x branch
# get_version_tuple exists in 2+
if hasattr(libgeos, 'version_regex'):
    libgeos.version_regex = version_regex
elif not hasattr(libgeos, 'get_version_tuple'):
    libgeos.geos_version_info = geos_version_info
