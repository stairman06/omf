import sys
import zipfile
import json
import os

def convert_file(mr_file):
    return {
        "fileType": "raw",
        "id": os.path.basename(mr_file['path']),
        "path": mr_file['path'],
        "downloads": mr_file['downloads'],
        "hashes": mr_file['hashes'],
        "fileSize": mr_file['fileSize'],
        "env": mr_file['env']
    }

if len(sys.argv) < 3:
    print('Please provide an mrpackfile to convert, and a file to output')
    print('Syntax: python ' + sys.argv[0] + ' <mrpack_file> <omf_output>')
    exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

input_pack = zipfile.ZipFile(input_path, 'r')

with input_pack.open('modrinth.index.json') as mrij:
    index = json.loads(mrij.read())

    output_index = {
        "formatType": "omf:pack",
        "formatVersion": 0,

        "meta": {
            "omf:project.name": index['name'],
            "omf:version.id": index['versionId']
        },

        "components": index['dependencies'],
        "files": list(map(convert_file, index['files']))
    }

    if index['summary'] is not None:
        output_index['meta']['omf:project.summary'] = index['summary']
    
    with zipfile.ZipFile(output_path, 'w') as o:
        # https://stackoverflow.com/a/16311587
        o.writestr('index.omf.json', json.dumps(output_index, separators=(',', ':')))

        # Copy all the overrides
        for file_name in input_pack.namelist():
            if file_name != 'modrinth.index.json':
                f = input_pack.open(file_name).read()
                o.writestr(file_name, f)
        

print('Successfully converted to OMF pack!')