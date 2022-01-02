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

import sys
import ijson

def load_wikidata():

    id_item = {}
    fh = open('/home/jordi/sc/diccionari-multilingue/sources/wikidata/terms.json', 'r')
    items = ijson.items(fh, 'item', use_float=True)        

    return items

def get_synset31_id(item):
    
    synset_id = None

    property_keys = item['claims']['P8814']
    for property_key in property_keys:
        if 'mainsnak' not in property_key:
            continue

        synset_id = property_key['mainsnak']['datavalue']['value']
        break

    return synset_id

def get_label_description(item, language):
    label = ''
    description = ''

    try:
        label = item['labels'][language]['value']
        if language in item['descriptions']:
            description = item['descriptions'][language]['value']
        
    except:
        pass

    return label, description


def wikidata_todict(items):
    id_item = {}
    
    for item in items:
        en_label, en_description = get_label_description(item, 'en')
        synset_id = get_synset31_id(item)

        new_item = {}

        label, description = get_label_description(item, 'en')
        new_item['en_label'] = label
        new_item['en_description'] = description

        label, description = get_label_description(item, 'ca')
        new_item['ca_label'] = label
        new_item['ca_description'] = description

        label, description = get_label_description(item, 'es')
        new_item['es_label'] = label
        new_item['es_description'] = description
        new_item['id'] = synset_id

        id_item[synset_id] = new_item

    return id_item

