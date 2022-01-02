#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import json


def load_term(filename, sysnet_prefix):
    WORD = 0
    CAT_ID = 2

    synset_ids = {}

    # Format 'Brussel·les	1	cat-30-08850450-n	n	99.0	None	------'
    with open(filename) as f:
        lines = [line.rstrip() for line in f]

    total = 0
    for line in lines:
        if line[0] == '#':
            continue

        total += 1
        components = line.split('\t')
        word = components[WORD].strip()
        cat_synset_id = components[CAT_ID].strip()
        synset_id = cat_synset_id.replace(sysnet_prefix, '')
        
        if synset_id in synset_ids:
            ids = synset_ids[synset_id]
            ids.append(word)
            synset_ids[synset_id] = ids
        else:
            words = [word]
            synset_ids[synset_id] = words
      
    for synset_id in synset_ids.keys():
#        print(f"'{synset_id}'")
        for value in synset_ids[synset_id]:
#            print(f" {value}")
            continue

    print(f"load_term {len(synset_ids)} from {total} entries")
    return synset_ids


def load_definitions(filename, sysnet_prefix):

    DEFINITION = 6
    CAT_ID = 0
    synset_ids = {}
    total = 0

    # Format 'cat-30-00001740-n	n	82546	-	-	0	Realitat considerada per abstracció com a unitat (amb o sense vida)	19	0	------'
    with open(filename) as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        if line[0] == '#':
            continue

        total += 1
        components = line.split('\t')
        definition = components[DEFINITION].strip()

        cat_synset_id = components[CAT_ID].strip()
        synset_id = cat_synset_id.replace(sysnet_prefix, '')
        if definition == 'None' or len(definition) == 0:
            continue

        #print(synset_id)
        synset_ids[synset_id] = definition

    for synset_id in synset_ids.keys():
        #print(f"'{synset_id}'")
        for value in synset_ids[synset_id]:
#            print(f" {value}")
            continue

    print(f"load_definitions {len(synset_ids)} from {total} entries")
    return synset_ids

def load_spanish():
    terms = load_term('data/3.0/es/wei_spa-30_variant.tsv', 'spa-30-')
    definitions = load_definitions('data/3.0/es/wei_spa-30_synset.tsv', 'spa-30-')
    return terms, definitions

def load_catalan():
    terms = load_term('data/3.0/ca/wei_cat-30_variant.tsv', 'cat-30-')
    definitions = load_definitions('data/3.0/ca/wei_cat-30_synset.tsv', 'cat-30-')
    return terms, definitions

def show_item(id, terms):
    print("---")
    print(f"id: {id}")
    for term in terms:
        print(f"term: {term}")

def main():

    catalan_def = 0
    spanish_def = 0

    terms_catalan, definitions_catalan = load_catalan()
    terms_spanish, definitions_spanish = load_spanish()
    terms = []

    for synset_id_spanish in terms_spanish:
#        print(terms_spanish[synset_id_spanish])

        ca_terms = []
        if synset_id_spanish in terms_catalan:
            catalan_def += 1
            for value in terms_catalan[synset_id_spanish]:
                ca_terms.append(value)
#                print(f"catalan: {value}")

        label_ca = ''
        if synset_id_spanish in definitions_catalan:
            label_ca = definitions_catalan[synset_id_spanish]

        # Spanish
        es_terms = []
        if synset_id_spanish in terms_spanish:
            for value in terms_spanish[synset_id_spanish]:
                es_terms.append(value)

        label_es = ''
        if synset_id_spanish in definitions_spanish:
            label_es = definitions_spanish[synset_id_spanish]

#        if len(ca_terms) == 0 or len(es_terms) == 0:
#            continue

#        if len(label_ca) == 0 and len(label_ca) == 0:
#            continue

        term = {}
        term['id'] = synset_id_spanish
        term['ca'] = ca_terms
        term['ca_label'] = label_ca
        term['es'] = es_terms
        term['es_label'] = label_es

        terms.append(term)

    print(f"Written {len(terms)}")
    
#    with open('terms-short.json', 'w') as outfile:
#        json.dump(terms[:200], outfile, indent=4, ensure_ascii=False)

    with open('terms.json', 'w') as outfile:
        json.dump(terms, outfile, indent=4, ensure_ascii=False)

    with open('words.txt', 'w') as outfile:
        for term in terms:
            outfile.write(f"{term['ca']} - {term['es']} - {term['ca_label']} - {term['es_label']}\n")

    with open('synset_ids_30.txt', 'w') as outfile:
        for term in terms:
            outfile.write(f"{term['id']}\n")
#            outfile.write(f"{term['id']} - {term['ca']} \n")

if __name__ == "__main__":
    main()
