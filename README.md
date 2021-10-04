# LinkedGeoData WordNet taxonomy alignment

This repository contains a rich taxonomy meant to better specify spatial entities in RDF. Even though there are projects like [LinkedGeoData](http://linkedgeodata.org) which provide or allow to generate huge amounts of spatio-semantic data, the underlying schema and taxonomy is quite shallow. The [taxonomy provided by LinkedGeoData](https://hobbitdata.informatik.uni-leipzig.de/LinkedGeoData/downloads.linkedgeodata.org/releases/2014-09-09/2014-09-09-ontology.sorted.nt.bz2) usually only contains at most three levels. For a richer taxonomy covering all kinds of spatial things we used [WordNet](https://wordnet.princeton.edu/) terms and their hypernymy relations to create a class hierarchy in RDF and linked the classes to the classes in LinkedGeoData.

## Lineage

### RDFization of WordNet terms and taxonomy

To generate a class hierarchy/taxonomy in RDF using the WordNet terms we make use of the [Prolog files provided by the WordNet project](https://wordnet.princeton.edu/documentation/prologdb5wn). The Prolog files `wn_hyp.pl` and `wn_s.pl`, respectively, contain information about hyperymy relations between synsets, and actual words linked to synsets. So, the entry

```Prolog
hyp(100001930,100001740).
```

says, that the synset `100001740` is a hypernym of synset `100001930`. With this information we create IRIs for each synset ID and RDF triples stating that the IRI of the first ID in the `hyp/2` predicate is a subclass of the IRI of the second one:

```Turtle
<http://sda.tech/wn/100001930> a <http://www.w3.org/2002/07/owl#Class> ;
    rdfs:subClassOf <http://sda.tech/wn/100001740> .
```

In the `wn_s.pl` file we can look up all words for a synset and add them as labels, e.g.

```Turtle
<http://sda.tech/wn/100001930> rdfs:label "physical entity" .
```

The Python script accomplishing this, can be found [here](scripts/mkclasses.py).

### LinkedGeoData taxonomy

To get all classes defined in the LinkedGeoData ontology we refer to the latest ontology file available on the [LinkedGeoData project website](https://hobbitdata.informatik.uni-leipzig.de/LinkedGeoData/downloads.linkedgeodata.org/releases/2014-09-09/2014-09-09-ontology.sorted.nt.bz2). In a first preprocessing step, we removed all labels using a simple `grep` command:

```bash
grep -v 'http://www.w3.org/2000/01/rdf-schema#label' 2014-09-09-ontology.sorted.nt > lgd_ontology_wo_labels.nt
```

This is done for two reasons. First, the labels are provided in many different language and for the linking step we are only interested in the English labels. Second, not all resources have labels so we decided to generate English labels in a uniform way. Here, we make use of the local parts of the IRIs which usually correspond to the labels, written in camel case. So to get English labels in a canonical way, we take the local part, e.g. `AmbulanceStation` from the IRI `<http://linkedgeodata.org/ontology/AmbulanceStation>` and 'undo' the camel case, getting 'ambulance station' which will be used as new label for `<http://linkedgeodata.org/ontology/AmbulanceStation>`. The label generation of the LinkedGeoData ontology _without any class labels_ is done by the [createlgdlabels.py script provided in this repo](scripts/createlgdlabels.py).

### Linking both taxonomies

To link both the WordNet and the LinkedGeoData taxonomies we used the [LIMES linking tool](https://github.com/dice-group/LIMES). LIMES proposes links based on a configured similarity score which holds between two resources of the respective input data sets. To link the WordNet and LinkedGeoData ontologies we used the trigram similarity of the classes' labels and we link them via the `rdfs:subClassOf` property. LIMES will create an N-Triples file containing all the additional `rdfs:subClassOf` statements. After merging all three datasets, i.e. the LinkedGeoData ontology, the WordNet taxonomy and the LIMES output, we have an integrated ontology combining and relating the class hierarchies of LinkedGeoData and WordNet. However, this automatically generated hierarchy may (and will) contain false `rdfs:subClassOf` relations as the generation only considered the bare labels. This means that a manual curation step has to follow, e.g. to remove `rdfs:subClassOf` relations between resources that have similar labels but are unrelated w.r.t their meaning. The LIMES configuration is [provided in this repo](config/limes_lgd_wn.xml).

### Manual curation

In the manual creation step we removed all WordNet classes which are not superclasses of a LinkedGeoData class. Further we checked all direct `rdfs:subClassOf` relations between a LinkedGeoData (sub-) and WordNet (super-) class and removed those which seemed inappropriate (e.g. since both classes refer to different concepts/meanings even though their labels are similar). The result of this manual cleaning step is provided [in the data folder](data/lgd_wn_taxonomy.ttl) in this repository.

## Combining the class hierarchy with additional spatial data

- http://download.geofabrik.de/ (e.g. Cologne: http://download.geofabrik.de/europe/germany/nordrhein-westfalen/koeln-regbez.html)
- Load into PostgreSQL with PostGIS extension using `osm2pgsql` (https://osm2pgsql.org/)
- Sparqlify (https://github.com/SmartDataAnalytics/Sparqlify)
- Example mappings for POIs with bounding box

## License

As this taxonomy is derived from WordNet and OpenStreetmap the following licenses apply:

- [WordNet 3.0 license](https://wordnet.princeton.edu/license-and-commercial-use)
- [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/)


## Open Issues

- Hypernym semantics don't always match `rdfs:subClassOf` semantics
- Multiple super classes mean that the sub class is on the intersection of them which does not always match the intended meaning of the original WordNet data
- Shops can be better linked to the concepts covering what is sold there, but this cannot be modeled by a `rdfs:subClassOf` relation
