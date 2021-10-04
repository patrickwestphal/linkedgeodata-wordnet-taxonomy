#!/usr/bin/env python3

from rdflib import Graph, Literal, OWL, RDF, RDFS, URIRef

HYPERNYM_FILE_PATH = 'wn_hyp.pl'
SENSE_FILE_PATH = 'wn_s.pl'
OUTPUT_FILE_PATH = 'wn_schema.ttl'
URI_PREFIX = 'http://sda.tech/wn/'


def get_hypernyms():
    # Typical line in the hypernyms file:
    # hyp(202172888,202176268).
    id_offset_begin = len('hyp(')
    id_offset_end = len(').')

    has_hypernyms = {}

    with open(HYPERNYM_FILE_PATH) as hypernyms_file:
        for line in hypernyms_file:
            # hyp(202172888,202176268).
            line = line.strip()[id_offset_begin:-id_offset_end]
            sub_id, super_id = line.split(',')

            if has_hypernyms.get(sub_id) is None:
                has_hypernyms[sub_id] = set()

            has_hypernyms[sub_id].add(super_id)

    return has_hypernyms


def mk_rdf_class_hierarchy(has_hypernyms) -> Graph:
    # Typical lines of the senses file:
    # s(100002137,1,'abstraction',n,6,0).
    # s(100002137,2,'abstract entity',n,1,0).
    # s(100002452,1,'thing',n,12,0).
    # s(100002684,1,'object',n,1,51).
    # s(100002684,2,'physical object',n,1,0).
    # s(100003553,1,'whole',n,2,0).
    # s(100003553,2,'unit',n,6,0).
    content_offset_begin = len('s(')
    content_offset_end = len(').')

    g = Graph()


    with open(SENSE_FILE_PATH) as senses_file:
        for line in senses_file:
            line = line[content_offset_begin:-content_offset_end]

            if not line.strip():
                continue
            
            parts = line.split(',')

            if len(parts) == 6:
                synset_id, label_nr, quoted_label, synset_type, _, _ = parts

            elif len(parts) == 4:
                synset_id, label_nr, quoted_label, synset_type, = parts

            if not synset_type == 'n':
                continue

            cls = URIRef(URI_PREFIX + synset_id)
            g.add((cls, RDF.type, OWL.Class))

            label = Literal(quoted_label[1:-1])
            g.add((cls, RDFS.label, label))
            
            hypernyms = has_hypernyms.get(synset_id)

            if hypernyms is not None:
                for hypernym_id in has_hypernyms[synset_id]:
                    super_cls = URIRef(URI_PREFIX + hypernym_id)
                    g.add((cls, RDFS.subClassOf, super_cls))

    return g


def main():
    has_hypernyms = get_hypernyms()

    class_hierarchy = mk_rdf_class_hierarchy(has_hypernyms)

    class_hierarchy.serialize(OUTPUT_FILE_PATH, format='turtle')


if __name__ == '__main__':
    main()

