#!/usr/bin/env python3

from argparse import ArgumentParser
from urllib.parse import unquote

import inflection
from rdflib import Graph
from rdflib import Literal
from rdflib import OWL
from rdflib import RDF
from rdflib import RDFS


def main(input_file_path: str, output_file_path: str):
    g = Graph()
    class_labels_g = Graph()

    with open(input_file_path) as input_file:
        g.load(input_file, format='ntriples')

        for s, p, o in g:
            if p == RDF.type and o == OWL.Class:
                label_str = inflection.underscore(
                        unquote(s.rsplit('/', 1)[-1])).replace('_', ' ')

                class_labels_g.add((s, RDFS.label, Literal(label_str)))

    g += class_labels_g

    with open(output_file_path, 'wb') as output_file:
        g.serialize(output_file, format='turtle')


if __name__ == '__main__':
    arg_parser = ArgumentParser()

    arg_parser.add_argument('input_file')
    arg_parser.add_argument('output_file')

    args = arg_parser.parse_args()

    main(args.input_file, args.output_file)
