from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
from datetime import datetime
import json

def convert_version_snippet(version):
    return {
        "id": version['id'],
        "src": f"http://localhost:8080/version/{version['id']}",

        "releaseDate": version['date_published'],
        "name": version['name'],
        "changelog": version['changelog'],
        "components": convert_components(version['game_versions'], version['loaders']),
        "relations": convert_relations(version['dependencies']),
        "x-modrinth": {
            "id": version['id']
        }
    }

def get_modrinth_versions(project):
    with urlopen(f'https://api.modrinth.com/v2/project/{project}/version') as raw:
        mr = json.load(raw)

        return list(map(convert_version_snippet, mr))

# http://docs.modrinth.com/api-spec/#operation/getProject
def get_modrinth_project(project):
    with urlopen(f'https://api.modrinth.com/v2/project/{project}') as raw:
        mr = json.load(raw)

        return {
            "formatType": "project",
            "formatVersion": 0,
            "meta": {
                "id": mr['id'],
                "name": mr['title'],
                "summary": mr['description'],
                "releaseDate": mr['published'],
                "x-modrinth": {
                    "id": mr['id'],
                    "slug": mr['slug']
                }
            },
            "versions": get_modrinth_versions(project)
        }


def convert_components(game_versions, loaders):
    out = []

    for loader in loaders:
        if loader == 'forge':
            out.append({
                "minecraft": game_versions,
                "forge": "*"
            })
        elif loader == 'fabric':
            out.append({
                "minecraft": game_versions,
                "fabric-loader": "*"
            })
        elif loader == 'quilt':
            out.append({
                "minecraft": game_versions,
                "quilt-loader": "*"
            })

    return out


def convert_relations(dependencies):
    out = []
    for dependency in dependencies:
        relation_type = dependency['dependency_type']
        if relation_type == 'incompatible':
            relation_type = 'conflicts'
        elif relation_type == 'optional':
            relation_type = 'recommends'

        out.append({
            "type": relation_type,
            "project": {
                "id": dependency['project_id'],
                "x-modrinth": {
                    "id": dependency['project_id']
                }
            },
            "version": {
                "src": f"http://localhost:8080/version/{dependency['version_id']}",
                "id": dependency['version_id'],
                "x-modrinth": {
                    "id": dependency['version_id']
                }
            }
        })

    return out


def convert_version_file(file):
    return {
        "primary": file['primary'],
        "type": "raw",
        "dest": f"mods/{file['filename']}",
        "downloads": [file['url']],
        "hashes": file['hashes'],
        "size": file['size']
    }


def get_modrinth_version(version):
    with urlopen(f'https://api.modrinth.com/v2/version/{version}') as raw:
        mr = json.load(raw)

        return {
            "formatType": "version",
            "formatVersion": 0,
            "project": {
                "id": mr['project_id'],
                "src": f"http://localhost:8080/project/{mr['project_id']}",
                "x-modrinth": {
                    "id": mr['project_id']
                }
            },
            "version": {
                "id": mr['id'],
                "name": mr['name'],
                "releaseDate": mr['date_published'],
                "components": convert_components(mr['game_versions'], mr['loaders']),
                "relations": convert_relations(mr['dependencies']),
                "x-modrinth": {
                    "id": mr['id']
                }
            },
            "files": list(map(convert_version_file, mr['files']))
        }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if self.path.startswith('/project/'):
            project_id = self.path.split('/')[2]

            out = json.dumps(get_modrinth_project(project_id))
            self.wfile.write(bytes(out, 'UTF-8'))
        elif self.path.startswith('/version/'):
            version_id = self.path.split('/')[2]

            out = json.dumps(get_modrinth_version(version_id))
            self.wfile.write(bytes(out, 'UTF-8'))


server = HTTPServer(('', 8080), Handler)

print('Modrinth proxy started on :8080')
server.serve_forever()
