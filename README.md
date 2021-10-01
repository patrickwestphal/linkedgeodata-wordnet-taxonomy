# LinkedGeoData WordNet taxonomy alignment

This repository contains a rich taxonomy meant to better specify spatial entities in RDF. Even though there are projects like [LinkedGeoData](http://linkedgeodata.org) which provide or allow to generate huge amounts of spatio-semantic data, the underlying schema and taxonomy is quite shallow. The [taxonomy provided by LinkedGeoData](https://hobbitdata.informatik.uni-leipzig.de/LinkedGeoData/downloads.linkedgeodata.org/releases/2014-09-09/2014-09-09-ontology.sorted.nt.bz2) usually only contains at most three levels. For a richer taxonomy covering all kinds of spatial things we used [WordNet](https://wordnet.princeton.edu/) terms and their hypernymy relations to create a class hierarchy in RDF and linked the classes to the classes in LinkedGeoData.

## Lineage

### RDFization of WordNet terms and taxonomy

### LinkedGeoData taxonomy

- Label cleaning

### Linking both taxonomies

### Manual curation

## License

As this taxonomy is derived from WordNet and OpenStreetmap the following licenses apply:

- [WordNet 3.0 license](https://wordnet.princeton.edu/license-and-commercial-use)
- [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/)


## Open Issues

- Hypernym semantics don't always match `rdf:subClassOf' semantics
- Multiple super classes mean that the sub class is on the intersection of them which does not always match the intended meaning of the original WordNet data
- Shops can be better linked to the concepts covering what is sold there, but this cannot be modeled by a `rdfs:subClassOf' relation
