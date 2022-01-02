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
import wikidata

# Read the subjects from WordNet 3.1 since they are not avaible in 3.0
def read_subjects_and_keymapping():
    mappings = {}
    subjects = {}
    with open('/home/jordi/sc/diccionari-multilingue/sources/wordnet/wordnet31-catalan/produced/synset_ids_31.txt', 'r') as fh:
        lines = fh.readlines()

        for line in lines:
            components = line.split('\t')
            key_31 = components[0].strip()
            key_30 = components[1].strip()
            subject = components[2].strip()
            subjects[key_30] = subject
            mappings[key_31] = key_30


    print(f"Read {len(subjects)} subjects")
    return mappings, subjects


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
        word = components[WORD].strip().replace("_", " ")
        cat_synset_id = components[CAT_ID].strip()
        synset_id = cat_synset_id.replace(sysnet_prefix, '')

        source = components[5].strip()
        if source == 'mw-maj-wikipedia': # Mainly noun names
            continue
       
        if synset_id in synset_ids:
            ids = synset_ids[synset_id]
            ids.append(word)
            synset_ids[synset_id] = ids
        else:
            words = [word]
            synset_ids[synset_id] = words
      
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

'''
    Returns
        word -> id
'''
def load_term_and_id(filename, sysnet_prefix):
    WORD = 0
    CAT_ID = 2

    terms = []

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
        
        term = {}
        term['word'] = word
        term['id'] = synset_id
        terms.append(term)

    print(f"load_term_and_id {len(terms)}")
    return terms

def is_valid_subject(subject):
    
    if 'noun.location' == subject:
        return False

    if 'noun.person' == subject:
        return False

    if 'noun.group' == subject:
        return False

    return True

def main():

    print("Reads Catalan Wordnet 3.0 and creates a JSON suitable to represent a Catalan - Spanish dictionary")

    catalan_def = 0
    spanish_def = 0

    terms_catalan, definitions_catalan = load_catalan()
    terms_spanish, definitions_spanish = load_spanish()
    entries = []

    # Catalan to Spanish
    catalan_terms_sequential = load_term_and_id('data/3.0/ca/wei_cat-30_variant.tsv', 'cat-30-')
    key31_to_key30, subjects = read_subjects_and_keymapping()

    last_word = None
    last_entry = []
    senses = 0

    for catalan_term_sequential in catalan_terms_sequential:
        sysnet_id = catalan_term_sequential['id']
        word = catalan_term_sequential['word']

        if sysnet_id not in terms_spanish:
            continue

        term = {}
        term['id'] = sysnet_id

        if sysnet_id in subjects:
            subject = subjects.get(sysnet_id)

            if is_valid_subject(subject) is False:
                continue
          
            term['subject'] = subject

        if last_word == word:
            entry = last_entry
        else:
            entry = []
            entries.append(entry)


        term['ca'] = word
        definition = definitions_catalan.get(sysnet_id)
        if definition:
            term['ca_definition'] = definition
            catalan_def += 1

        term['es'] = terms_spanish[sysnet_id]

        definition = definitions_spanish.get(sysnet_id)
        if definition:
            term['es_definition'] = definition
            spanish_def += 1

        senses += 1
        entry.append(term)

        last_word = word
        last_entry = entry

    
    with open('terms-short.json', 'w') as outfile:
        json.dump(entries[:5000], outfile, indent=4, ensure_ascii=False)

    with open('terms.json', 'w') as outfile:
        json.dump(entries, outfile, indent=4, ensure_ascii=False)

    with open('words.txt', 'w') as outfile:
        for term in entries:
            outfile.write(f"{term}\n")

    print("--- Stats")
    print(f"{len(entries)} dictionary entries with {senses} senses")
    pspanish_def = spanish_def * 100 / senses
    pcatalan_def = catalan_def * 100 / senses
    print(f"{spanish_def} ({pspanish_def:.2f}%) senses with Spanish definition, Catalan {catalan_def} ({pcatalan_def:.2f}%)")

if __name__ == "__main__":
    main()
