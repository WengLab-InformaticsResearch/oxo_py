""" Basic implementation of EMBL-EBI's OxO mappings in Python using mapping files provided by EMBL-EBI.

https://www.ebi.ac.uk/spot/oxo/index

Notes:
    The mapping algorithm may be different from OxO's. A few test cases have been run and produced matching results.

    Update OxO._file_ols and OxO._file_umls with the location of the mapping files provided by EMBL-EBI.

Examples:
    OxO.find_mappings('DOID:162')
    OxO.find_mappings('UMLS:C0002199', distance=3)
    OxO.find_mappings('SNOMEDCT:136111001', distance=3, targets=['MeSH', 'UMLS'])
"""

import csv
from collections import defaultdict


class OxO:
    _mappings = None
    _terms = None
    _file_ols = r'D:\oxo\ols_mappings.csv'
    _file_umls = r'D:\oxo\umls_mappings.csv'
    _file_terms = r'D:\oxo\terms.csv'

    @staticmethod
    def load_files():
        # Initialize
        OxO._terms = dict()
        OxO._mappings = defaultdict(set)

        # Read in the terms
        with open(OxO._file_terms, 'r', newline='') as fh:
            reader = csv.reader(fh, delimiter=',', quotechar='"', doublequote=False, lineterminator='\r\n',
                                escapechar='\\')

            # Skip the header line
            reader.__next__()

            # Read in term definitions
            for identifier, curie, label, uri, prefix in reader:
                OxO._terms[curie] = {
                    'label': label,
                    'uri': uri,
                }

                # Read in OLS dump file using csv reader
        with open(OxO._file_ols, 'r', newline='') as fh:
            reader = csv.reader(fh, delimiter=',', quotechar='"', doublequote=False, lineterminator='\r\n',
                                escapechar='\\')

            # Skip the header line
            reader.__next__()

            # Read in all mappings
            for row in reader:
                curie_from = row[0]
                curie_to = row[1]
                OxO._mappings[curie_from].add(curie_to)
                OxO._mappings[curie_to].add(curie_from)

        # Read in UMLS dump file using csv reader
        with open(OxO._file_umls, 'r', newline='') as fh:
            reader = csv.reader(fh, delimiter=',', quotechar='"', doublequote=False, lineterminator='\r\n',
                                escapechar='\\')

            # Skip the header line
            reader.__next__()

            # Read in all mappings
            for row in reader:
                curie_from = row[0]
                curie_to = row[1]
                OxO._mappings[curie_from].add(curie_to)
                OxO._mappings[curie_to].add(curie_from)

    @staticmethod
    def find_mappings(curie_source, distance=2, targets=None):
        if OxO._mappings is None:
            OxO.load_files()

        found = dict()  # mapping results (key:curie, value:distance)
        visited = set()  # nodes already visited
        searching = {curie_source}  # nodes to visit on this iteration
        prefix_source = curie_source.split(':')[0]

        # Convert targets to a set
        if targets is None:
            targets = []
        elif type(targets) is str:
            targets = [targets]
        targets = set(targets)

        for i in range(distance):
            search_add = set()  # nodes to search in the next iteration

            # Mark all nodes that we're about to visit as already visited
            visited = visited.union(searching)

            # Visit each new node
            for curie in searching:
                curr_mappings = OxO._mappings[curie]

                # Add new mappings to the set to search in the next iteration if we have not already visited
                search_add = search_add.union([x for x in curr_mappings if x not in visited])

                # Add new mappings to the set of found mappings if it's in the target ontologies
                for m in curr_mappings:
                    prefix_curr = m.split(':')[0]
                    if m not in found and prefix_curr != prefix_source and \
                            (len(targets) == 0 or prefix_curr in targets):
                        info = {
                            'distance': i + 1,
                            'label': '',
                            'uri': ''
                        }

                        if m in OxO._terms:
                            term = OxO._terms[m]
                            info['label'] = term['label']
                            info['uri'] = term['uri']

                        found[m] = info

            searching = search_add

        return found
