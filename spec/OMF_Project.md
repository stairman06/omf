# OMF Projects
OMF Projects allow you to represent metadata for a Minecraft mod or modpack. OMF Projects are a JSON-based format that let you make available as much or as little metadata as necessary. The following are the available properties for this format.

## `formatType`
This property MUST be set to `omf:project`

## `formatVersion`
This property MUST be set to `0`. Future versions will increment this number.

## `meta` (optional)
A [Project Metadata Reference](./Metadata_References.md#project-metadata-references) object for this file.

## `versions`
A list of all versions of this Project. Each object in this array contains the following properties

### `id`
A unique identifier for this version. This MUST NOT be used for any other version.

### `src`
A URL which returns Version Metadata for this version

### `meta` (optional)
A [Version Metadata Reference](./Metadata_References.md#version-metadata-references) object for this version. This allows you to specify things like version name, required components, dependencies, release date, and more.