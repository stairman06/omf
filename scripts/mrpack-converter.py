import sys
import zipfile
import json
import os

def convert_file_to_asset(mr_file):
    return {

        "id": os.path.basename(mr_file['path']),
        "type": "remote",
        "env": mr_file.get('env', {
            "client": "required",
            "server": "required"
        }),
        "file": {
            "type": "raw",
            "dest": mr_file['path'],
            "downloads": mr_file['downloads'],
            "hashes": mr_file['hashes'],
            "size": mr_file['fileSize'],
        },
    }

if len(sys.argv) < 3:
    print('Please provide an mrpack file to convert, and a file to output')
    print('Syntax: python ' + sys.argv[0] + ' <mrpack_file> <omf_output>')
    exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

input_pack = zipfile.ZipFile(input_path, 'r')

with input_pack.open('modrinth.index.json') as index_file:
    index = json.loads(index_file.read())

    output_index = {
        "formatType": "instance",
        "formatVersion": 0,

        "project": {
            "name": index['name'],
            "summary": index['summary']
        },
        "version": {
            "id": index['versionId']
        },
        "assets": list(map(convert_file_to_asset, index['files'])),
        "components": index['dependencies'],
    }

    with zipfile.ZipFile(output_path, 'w') as output_zip:
        # dump without spaces https://stackoverflow.com/a/16311587
        output_zip.writestr('instance.omf.json', json.dumps(output_index, separators=(',', ':')))

        # Copy all the overrides
        for file_name in input_pack.namelist():
            if file_name != 'modrinth.index.json':
                f = input_pack.open(file_name).read()
                output_zip.writestr(file_name, f)
        
print('Successfully converted to OMF instance!')