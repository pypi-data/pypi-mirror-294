"""Taxref common module"""

from collections import namedtuple

PdReadCts = namedtuple(typename='PdReadCts',
                       field_names=['sep', 'encoding_errors', 'header', 'index_col', 'dtype', 'na_filter'])

# default reader constants for most of Taxref versions
STRICT = PdReadCts(sep='\t',
                   encoding_errors='strict',
                   header=0,
                   index_col='CD_NOM',
                   dtype={
                          'CD_NOM': 'string'
                      },
                   na_filter=False)

IGNORE = PdReadCts(sep='\t',
                   encoding_errors='ignore',
                   header=0,
                   index_col='CD_NOM',
                   dtype={
                           'CD_NOM': 'string'
                       },
                   na_filter=False)
