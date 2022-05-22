# Open Minecraft Formats
OMF is a set of experimental open formats for modded Minecraft tools.

All formats are currently in beta, version `0`. 

## OMF Pack (`omf:pack`)
OMF Packs are a simple ZIP-based format for the storage of modpacks. [View the specification](./spec/OMF_Pack.md)

## OMF Project (`omf:project`)
OMF Projects are a metadata format for representing Minecraft mods and modpacks, and where to download them. [View the specification](./spec/OMF_Project.md)

## OMF Version (`omf:version`)
OMF Versions are individual versions, referenced in the OMF Project specification, that specify the actual individual files that can be downloaded. [View the specification](./spec/OMF_Version.md)

## Metadata References
All OMF formats make use of [Metadata References](./spec/Metadata_References.md), which allow one to specify metadata such as names, IDs, release dates, changelogs, dependencies, and more through the use of namespaced keys. All OMF keys use the `omf:` namespace.

## Examples
Examples can be found in the `examples/` directory. 

`example-mod-meta` is an example Project and Version metadata for a mod  
`example-pack-meta` is an example Project and Version metadata for a pack  
`example-pack` is an example OMF Pack, just extracted. To turn it into a `.omfpack`, simply zip the contents

## JSON Schema
JSON schemas are provided in the `schema/` directory. Note that all schemas require the `meta.schema.json` file.

## Scripts
The `scripts/` directory contains simple tools. 

Currently, only `mrpack-convertor.py` exists, which allows you to convert an mrpack to an OMF Pack:

```
python scripts/mrpack-convertor.py input.mrpack output.omfpack
```