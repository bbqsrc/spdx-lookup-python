spdx-lookup
===========

A tool to query the SPDX license list.

Usage
-----

API
~~~

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

Command-line tool
~~~~~~~~~~~~~~~~~

::

    usage: spdx-lookup [-h] (-i ID | -n NAME | -d DIR | -f FILE)
                       {template,info} ...

    optional arguments:
      -h, --help            show this help message and exit

    Lookup method:
      -i ID, --id ID        Find license with given identifier
      -n NAME, --name NAME  Find license with given name
      -d DIR, --dir DIR     Search directory for valid license
      -f FILE, --file FILE  Read file to detect license

    Actions:
      {template,info}
        template            print license template
        info                print metadata about license

License
-------

BSD 2-clause. See LICENSE.
