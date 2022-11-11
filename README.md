# Open Minecraft Formats
OMF is a set of experimental open formats for modded Minecraft tools.

All formats are currently a draft, version `0`. 

## OMF Instances (`instance`)
OMF Instances are a simple zip-based format for the storage of portable Minecraft instances. [View the specification](./spec/OMF_Instance.md)

## OMF Projects (`project`)
OMF Projects are a metadata format for representing Minecraft mods and modpacks, and where to download them. [View the specification](./spec/OMF_Project.md)

## OMF Versions (`version`)
OMF Versions are individual versions, referenced in the OMF Project specification, that specify the actual individual files that can be downloaded. [View the specification](./spec/OMF_Version.md)

## OMF Components (`component`)
OMF Components are a structured way to define standard libraries, arguments, Java agents and main classes required by Minecraft modloaders or other tools. [View the specification](./spec/OMF_Components.md)

## Examples
Examples can be found in the `examples/` directory. 
    
`example-mod-meta` is an example project and version metadata for a mod  
`example-pack-meta` is an example project and version metadata for a modpack  
`example-pack` is an example OMF Instance, just extracted. To turn it into a `.omfinstance`, simply zip the contents  
`example-component.omf.json` is an example OMF Component  

## JSON Schema
JSON schemas are provided in the `schema/` directory. Note that all schemas require the `meta.schema.json` file.

## Scripts
The `scripts/` directory contains simple tools. 

`mrpack-converter.py` allows you to convert an mrpack to an OMF Instance:

```
python scripts/mrpack-convertor.py input.mrpack output.omfpack
```

`modrinth-proxy.py` is a proxy for Modrinth. All requests are on `localhost:8080`. For example, to get Sodium's OMF representation: `localhost:8080/project/sodium`