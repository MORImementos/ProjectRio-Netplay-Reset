import json
import re

def dmw_to_py():
    datatypes = ['byte', 'halfword', 'word', 'float', 'double', 'string', 'byte_array']

    import json

    with open('AutoReset.dmw', 'r') as f:
        data = json.load(f)['watchList']

    addr = {}

    for i in data:
        address = i.get('address')
        if address:
            label = i.get('label')
            label = re.sub('\s', '_', label)

            length = i.get('length')
            addr[label] = {'address': address, 'type': datatypes[i.get('typeIndex')], 'unsigned': i.get('unsigned'), 'length': length}
        else:
            groupEntries = i.get('groupEntries')
            if groupEntries:
                groupname = i.get('groupName')
                groupname = re.sub('\s', '_', groupname)
                for entry in groupEntries:
                    address = entry.get('address')
                    if address:
                        label = entry.get('label')
                        label = re.sub('\s', '_', label)

                        length = entry.get('length')
                        addr[groupname + "." + label] = {'address': address, 'type': datatypes[entry.get('typeIndex')], 'unsigned': entry.get('unsigned'), 'length': length}


    clean_dict = {}
    for k, v in addr.items():
        clean_label = re.sub(r'[^a-zA-Z0-9_]', '_', k)
        clean_label = re.sub(r'[? ,/.()]', '_', clean_label)
        clean_label = re.sub(r'[-_]', '_', clean_label)
        clean_label = re.sub(r'^(\d)', r'_\1', clean_label).lower().rstrip('_')

        clean_dict[clean_label] = addr[k]

    print(clean_dict)

    with open('dme_addresses.py', 'w') as f:
        for label, info in clean_dict.items():
            address = '0x' + str(info['address'])
            unsigned = 'u' if info['unsigned'] else ''
            datatype = info['type']
            if info['length']:
                length = info['length']
                f.write(f"{label} = {address} # {unsigned}{datatype}_{length}\n")
            else:
                f.write(f"{label} = {address} # {unsigned}{datatype}\n")


    print("Labels written to dme_addresses.py")

dmw_to_py()