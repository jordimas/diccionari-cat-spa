import xml.etree.ElementTree as ET
import json
import unicodedata

# http://wordnetweb.princeton.edu/
# http://compling.hss.ntu.edu.sg/omw/cgi-bin/wn-gridx.cgi?usrname=&gridmode=grid



def load_term_spanish():
    WORD = 0
    CAT_ID = 2

    synset_ids = {}

    # Format 'Brussel·les	1	cat-30-08850450-n	n	99.0	None	------'
    with open('data/3.0/es/wei_spa-30_variant.tsv') as f:
        lines = [line.rstrip() for line in f]

    total = 0
    for line in lines:
        if line[0] == '#':
            continue

        total += 1
        components = line.split('\t')
        word = components[WORD].strip()
        cat_synset_id = components[CAT_ID].strip()
        synset_id = cat_synset_id.replace('spa-30-', '')
        
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

    print(f"load_term_spanish {len(synset_ids)} from {total} entries")
    return synset_ids


def load_definitions_spanish():

    DEFINITION = 6
    CAT_ID = 0
    synset_ids = {}
    total = 0

    # Format 'cat-30-00001740-n	n	82546	-	-	0	Realitat considerada per abstracció com a unitat (amb o sense vida)	19	0	------'
    with open('data/3.0/es/wei_spa-30_synset.tsv') as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        if line[0] == '#':
            continue

        total += 1
        components = line.split('\t')
        definition = components[DEFINITION].strip()

        cat_synset_id = components[CAT_ID].strip()
        synset_id = cat_synset_id.replace('spa-30-', '')
        if definition == 'None' or len(definition) == 0:
            continue

        #print(synset_id)
        synset_ids[synset_id] = definition

    for synset_id in synset_ids.keys():
        #print(f"'{synset_id}'")
        for value in synset_ids[synset_id]:
#            print(f" {value}")
            continue

    print(f"load_definitions_spanish {len(synset_ids)} from {total} entries")
    return synset_ids

def load_spanish():
    terms = load_term_spanish()
    definitions = load_definitions_spanish()
    return terms, definitions


def load_term_catalan():
    WORD = 0
    CAT_ID = 2

    synset_ids = {}
    total = 0

    # Format 'Brussel·les	1	cat-30-08850450-n	n	99.0	None	------'
    with open('data/3.0/ca/wei_cat-30_variant.tsv') as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        if line[0] == '#':
            continue

        total += 1
        components = line.split('\t')
        word = components[WORD].strip()
        cat_synset_id = components[CAT_ID].strip()
        synset_id = cat_synset_id.replace('cat-30-', '')
        
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

    print(f"load_term_catalan {len(synset_ids)} from {total} entries")
    return synset_ids


def load_definitions_catalan():

    DEFINITION = 6
    CAT_ID = 0
    synset_ids = {}
    total = 0

    # Format 'cat-30-00001740-n	n	82546	-	-	0	Realitat considerada per abstracció com a unitat (amb o sense vida)	19	0	------'
    with open('data/3.0/ca/wei_cat-30_synset.tsv') as f:
        lines = [line.rstrip() for line in f]

    for line in lines:
        if line[0] == '#':
            continue

        total += 1
        components = line.split('\t')
        definition = components[DEFINITION].strip()

        cat_synset_id = components[CAT_ID].strip()
        synset_id = cat_synset_id.replace('cat-30-', '')
        if definition == 'None' or len(definition) == 0:
            continue

        #print(synset_id)
        synset_ids[synset_id] = definition

    for synset_id in synset_ids.keys():
        #print(f"'{synset_id}'")
        for value in synset_ids[synset_id]:
#            print(f" {value}")
            continue

    print(f"load_definitions_catalan {len(synset_ids)} from {total} entries")
    return synset_ids

def load_catalan():
    terms = load_term_catalan()
    definitions = load_definitions_catalan()
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
