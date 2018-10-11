# oxo_py
Basic implementation of [EMBL-EBI's Ontology Xref Service (OxO)](https://www.ebi.ac.uk/spot/oxo/index) mappings in Python using mapping files provided by EMBL-EBI.

The mapping algorithm may be different from OxO's. A few test cases have been run and produced matching results.


## Requirements

Python 3

[Mapping files](http://ftp.ebi.ac.uk/pub/databases/spot/oxo/)

## Notes

Update ```OxO._file_ols```, ```OxO._file_umls```, and ```OxO._file_terms``` with the location of the mapping files provided by EMBL-EBI.

The mappings files will be loaded on the first call to ```OxO.find_mappings()```. The files may take ~30 seconds to load. Alternatively, you can call ```OxO.load_files()``` to load the files at an earlier time. 

## Examples

```OxO.find_mappings('DOID:162')```

```OxO.find_mappings('UMLS:C0002199', distance=3)```

```OxO.find_mappings('SNOMEDCT:136111001', distance=3, targets=['MeSH', 'UMLS'])```

## Acknowledgements
Big thanks to [European Bioinformatics Institute](https://www.ebi.ac.uk/) for providing the OxO service and the OxO mapping files.