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
import sys
import ijson

#def save(values, append = False):
#    with open('terms.json', 'w') as outfile:
#        json.dump(values, outfile, skipkeys=True, indent=4, ensure_ascii=False)


def read_subjects():
    subjects = {}
    with open('/home/jordi/sc/diccionari-multilingue/sources/wordnet/wordnet31-catalan/produced/synset_ids_31.txt', 'r') as fh:
        lines = fh.readlines()

        for line in lines:
            components = line.split('\t')
            key_30 = components[1].strip()
            subject = components[2].strip()
            subjects[key_30] = subject

    print(f"Readed {len(subjects)} subjects")
    return subjects


def _load_wordnet():
    with open('terms.json', 'r') as fh:
        wordnet = json.load(fh)

    print(f"Wordnet read {len(wordnet)} items")
    return wordnet


def _wordnet_todict(wordnet):
    id_item = {}
    for item in wordnet:
        id = item['id']
#        new_id = item['id'][1:] + "-" + item['id'][0:1]
#        item['id'] = new_id
        id_item[id] = item

    return id_item

def show_item_wordnet(item):

    print("---")
    print(f"--- subject: {item['subject']} - {item['id']}")
    print(f"Català {item['ca']} -  {item['ca_label']} ")
    print(f"Castellà {item['es']} -  {item['es_label']} ")


def main():
    wordnet_list = _load_wordnet()
    wordnet_dict = _wordnet_todict(wordnet_list)
    subjects = read_subjects()

    entries = 0
    catalan_definition = 0
    spanish_definition = 0

    for sysnet30_id in wordnet_dict:
        item = wordnet_dict[sysnet30_id]
        if len(item['ca']) == 0 or len(item['es']) == 0:
            continue

        if len(item['ca_label']) == 0 and len(item['es_label']) == 0:
            continue

        subject = subjects.get(sysnet30_id)
        item['subject'] = subject

        if subject is not None:
            if 'noun.location' == subject:
                continue

            if 'noun.person' == subject:
                continue

        if len(item['ca_label']) > 0:
            catalan_definition += 1

        if len(item['es_label']) > 0:
            spanish_definition += 1
                    

        show_item_wordnet(item)
        entries += 1

    print(f"Entries {entries}, catalan_definition {catalan_definition}, spanish_definition {spanish_definition}")


if __name__ == "__main__":
    print("Generate Catalan - Spanish dictionary")
    main()
