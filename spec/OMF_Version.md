# OMF Versions
OMF Versions are a metadata format to provide information about a specific version of a Project. They have the following properties:

## `formatType`
This MUST be set to `version`

## `formatVersion`
This MUST be set to `0`. Future versions will increment this number.

## `project` (optional)
A [Project Metadata Reference](./Metadata_References.md#project-metadata-references) object for this version's corresponding project.

## `meta` (optional)
A [Version Metadata Reference](./Metadata_References.md#version-metadata-references) object for this version.

## `files`
An array consisting of [File Metadata References](./Metadata_References.md#file-metadata-references) for each file in this version. Each file MUST have the `type` field. It is RECOMMENDED that there be one file with the `primary` property set to `true`.