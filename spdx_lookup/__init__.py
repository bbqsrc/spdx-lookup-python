# coding=utf-8

from collections import namedtuple
import os
import re

import spdx
from spdx import License

LicenseMatch = namedtuple('LicenseMatch',
        ['confidence', 'license', 'filename'])

_id_idx = {}
_name_idx = {}

for n, record in enumerate(spdx._licenses):
    _name_idx[record['name'].lower().strip()] = n
    _id_idx[record['id'].lower().strip()] = n


_word_set_re = re.compile(r"([A-Za-z]+|[A-Za-z]+'[A-Za-z]+)")
_copyright_re = re.compile(r'\s*Copyright\s*(©|\(c\)|\xC2\xA9)?' +
                            '\s*(\d{4}|.year.)(.*)?' +
                            '(?:\s*All rights reserved).*', re.I | re.M)
_spdx_var_re = re.compile(r'<<var;name=(.*?);' +
                           'original=(.*?);match=(.*?)>>', re.I | re.M)


def _spdx_var_orig(match):
    return match.group(2)


def _spdx_var_match(match):
    return match.group(3)


def _get_word_set(content, spdx=False):
    x = _copyright_re.sub('', content.lower())
    if spdx:
        x = _spdx_var_re.sub(_spdx_var_orig, x)
    return set(_word_set_re.findall(x))


def by_name(name):
    q = name.strip().lower()
    i = _name_idx.get(q, None)

    if i is not None:
        return License(spdx._licenses[i])


def by_id(id_):
    q = id_.strip().lower()
    i = _id_idx.get(q, None)

    if i is not None:
        return License(spdx._licenses[i])


# Special cases for matching
_hidden = {
    'BSD-2-Clause-FreeBSD',
    'BSD-2-Clause-NetBSD',
    'Mup'
}


def _match_all(content, threshold=90, include_hidden=False):
    word_set = _get_word_set(content)
    max_delta = len(word_set) * threshold/100.0

    potentials = []
    for l in spdx._licenses:
        license = License(l)
        if license.id in _hidden and not include_hidden:
            continue

        license_ws = _get_word_set(license.template, True)
        delta = abs(len(word_set) - len(license_ws))

        if delta <= max_delta:
            potentials.append((delta, license, license_ws))

    potentials.sort(key=lambda x: x[0])
    potentials.reverse()

    matches = []
    for _, license, license_ws in potentials:
        overlap = len(word_set & license_ws)
        total = len(word_set) + len(license_ws)
        similarity = 100.0 * (overlap * 2.0 / total)

        if similarity >= threshold:
            matches.append((similarity, license))

    return sorted(matches, key=lambda x: x[0])


def match(content, threshold=90, include_hidden=False):
    matches = _match_all(content, threshold, include_hidden)
    if len(matches) == 0:
        return None

    m = matches.pop()
    return LicenseMatch(m[0], m[1], None)

_license_fn_res = [
    re.compile('^(un)?licen[sc]e$', re.I),
    re.compile('^(un)?licen[sc]e\.(md|markdown|txt)$', re.I),
    re.compile('^copy(ing|right)(\.[^.]+)?$', re.I),
    re.compile('^(un)?licen[sc]e\.[^.]+$', re.I),
    re.compile('licen[sc]e', re.I)
]

def _file_score(path):
    fn = os.path.basename(path)

    for n, regex in enumerate(_license_fn_res):
        if regex.match(fn):
            return len(_license_fn_res) - n
    return 0

def match_path(path, threshold=90, include_hidden=False):
    if not os.path.isdir(path):
        raise ValueError("Path must be a directory")

    x = []
    for fn in os.listdir(path):
        fnp = os.path.join(path, fn)
        score = _file_score(fnp)
        if score > 0:
            x.append((score, fn))

    if len(x) == 0:
        return None

    x.sort(key=lambda x: x[0])

    fn = x.pop()[1]
    with open(os.path.join(path, fn)) as f:
        matches = _match_all(f.read(), threshold, include_hidden)
        if len(matches) > 0:
            m = matches[0]
            return LicenseMatch(m[0], m[1], fn)

