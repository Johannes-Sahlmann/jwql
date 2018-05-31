#! /usr/bin/env python

"""Tests for the ``dbmonitor`` module.

Authors
-------

    Joe Filippazzo

Use
---

    These tests can be run via the command line (omit the ``-s`` to
    suppress verbose output to stdout):
    ::

        pytest -s test_dbmonitor.py
"""

from ..dbmonitor import dbmonitor as db
from ..utils.utils import JWST_INSTRUMENTS


def test_caom_instrument_keywords():
    """Test to see that the CAOM keywords are the same for all
    instruments"""
    kw = []
    for ins in JWST_INSTRUMENTS:
        kw.append(db.instrument_keywords(ins, caom=True)['keyword'].tolist())

    assert kw[0] == kw[1] == kw[2] == kw[3] == kw[4]


def test_filtered_instrument_keywords():
    """Test to see that the instrument specific service keywords are
    different for all instruments"""
    kw = []
    for ins in JWST_INSTRUMENTS:
        kw.append(db.instrument_keywords(ins, caom=False)['keyword'].tolist())

    assert kw[0] != kw[1] != kw[2] != kw[3] != kw[4]


def test_instrument_inventory_filtering():
    """Test to see that the instrument inventory can be filtered"""
    filt = 'GR150R'
    data = db.instrument_inventory('niriss',
                                   add_filters={'filter': filt},
                                   return_data=True)

    filters = [row['filter'] for row in data['data']]

    assert all([i == filt for i in filters])


def test_instrument_dataproduct_filtering():
    """Test to see that the instrument inventory can be filtered
    by data product"""
    dp = 'spectrum'
    data = db.instrument_inventory('nirspec', dataproduct=dp, caom=True,
                                   return_data=True)

    dps = [row['dataproduct_type'] for row in data['data']]

    assert all([i == dp for i in dps])
