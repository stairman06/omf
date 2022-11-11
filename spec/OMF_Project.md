# OMF Projects
OMF Projects allow you to represent metadata for a Minecraft mod or modpack. OMF Projects are a JSON-based format that let you make available as much or as little metadata as necessary. The following are the available properties for this format.

## `formatType`
This property MUST be set to `project`.

## `formatVersion`
This property MUST be set to `0`. Future versions will increment this number.

## `meta` (optional)
A [Project Metadata Reference](./Metadata_References.md#project-metadata-references) object for this project.

## `versions`
An array consisting of [Version Metadata References](./Metadata_References.md#version-metadata-references) for every available version of this project.

Each Version Metadata Reference is required to have the `id` field. It is RECOMMENDED to include the `src` field as well, in order to provide a more permanent source for the version metadata.