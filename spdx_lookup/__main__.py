import argparse
import textwrap
import sys

import spdx_lookup as lookup
from spdx_lookup import LicenseMatch, _spdx_var_re

MAX_WIDTH = 2 ** 20

def indent(text, prefix):
    w = textwrap.TextWrapper(initial_indent=prefix, subsequent_indent=prefix,
        expand_tabs=False, drop_whitespace=False, replace_whitespace=False,
        break_long_words=False, break_on_hyphens=False, width=MAX_WIDTH)
    return '\n'.join(w.fill(x) for x in text.split('\n'))

def wrap(text, w=77):
    return '\n'.join(textwrap.fill(x, w) for x in text.split('\n'))

def print_info(res):
    if isinstance(res, LicenseMatch):
        if res.filename:
            print("File: %s" % res.filename)
        print("Confidence: %.2f%%" % res.confidence)
        res = res.license

    print("Id: %s" % res.id)
    print("Name: %s" % res.name)
    print("OSI approved: %s" % ("yes" if res.osi_approved is True else "no"))
    if res.notes:
        print("Notes:")
        print(indent(wrap(res.notes), '  '))
    if res.header:
        print("Header:")
        print(indent(wrap(res.header), '  '))

def print_license(res):
    if isinstance(res, LicenseMatch):
        res = res.license
    tmpl = _spdx_var_re.sub(lambda x: x.group(2), res.template)
    print(wrap(tmpl, 80))

def main():
    p = argparse.ArgumentParser(prog='spdx-lookup')

    g = p.add_argument_group('Lookup method')
    x = g.add_mutually_exclusive_group(required=True)
    x.add_argument('-i', '--id', help='Find license with given identifier')
    x.add_argument('-n', '--name', help='Find license with given name')
    x.add_argument('-d', '--dir', help='Search directory for valid license')
    x.add_argument('-f', '--file', type=argparse.FileType('r'),
        help='Read file to detect license')

    g = p.add_subparsers(dest='action', title='Actions')
    g.required = True
    g.add_parser('template', help='print license template')
    g.add_parser('info', help='print metadata about license')

    args = p.parse_args()

    if args.id:
        res = lookup.by_id(args.id)
    elif args.name:
        res = lookup.by_name(args.name)
    elif args.dir:
        res = lookup.match_path(args.dir)
    elif args.file:
        res = lookup.match(args.file.read())
        args.file.close()

    if res is None:
        print("No supported license was detected.")
        return 1

    if args.action == 'info':
        print_info(res)
    elif args.action == 'template':
        print_license(res)

if __name__ == "__main__":
    import sys
    sys.exit(main())
