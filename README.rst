spdx-lookup
===========

A tool to query the SPDX license list.

Usage
-----

::

    import spdx_lookup as lookup

    # Case-insensitive SPDX id lookup
    lookup.by_id('gpl-3.0') # -> returns License object or None

    # Case-insensitive SPDX name lookup
    lookup.by_name('gpl-3.0') # -> returns License object or None

    # Find closest match for provided license content
    with open('some-license.txt') as f:
        match = lookup.match(f.read()) # -> returns LicenseMatch or None

    match.confidence # -> a float between 0 and 100
    match.license # -> a License object

License
-------

BSD 2-clause. See LICENSE.
