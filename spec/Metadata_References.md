# Metadata References
Metadata References are used through the OMF standard to allow standardized and non-standardized metadata to be referenced. Metadata References are objects consisting of namespaced keys and values.

Standardized metadata uses the `omf` namespace. Therefore, this namespace MUST NOT be used for any non-standard metadata.

Non-standardized metadata can use any namespace.

## Standard Keys
Standardized keys in the `omf` namespace are:

`omf:project.src`: URL where the full OMF Project Metadata can be found for the Project 
`omf:project.id` Project ID  
`omf:project.name`: Human readable name of the Project  
`omf:project.type`: Type of the Project. Available values are `mod` and `pack`  
`omf:project.releaseDate`: Unix timestamp representing the initial release of the Project
`omf:project.summary`: A short, one to two sentence summary of the Project

`omf:version.src`: URL where the full OMF Version Metadata can be found for the Version  
`omf:version.id`: Version ID  
`omf:version.name`: Human readable name of the Version
`omf:version.releaseDate`: Unix timestamp representing the initial release of the Version  
`omf:version.components`: Components required for the Version. [See the components definition in the OMF Pack format](./OMF_Pack.md#components)  
`omf:version.dependencies`: Dependencies required for the Version. Each dependency is an object consisting of a `type` (either `required` or `optional`), and an optional [Combined Metadata Reference](#combined-metadata-references) `meta` property

## Metadata Reference Types
There are 3 types of Metadata Reference objects.

### Project Metadata References
Project Metadata References are restricted to having `omf:project.*` keys for their standardized keys. Nonstandardized keys are still allowed as usual.

### Version Metadata References
Version Metadata References are restricted to having `omf:version.*` keys for their standardized keyts. Nonstandardized keys are still allowed as usual.

### Combined Metadata References
Combined Metadata References can have any `omf:` standardized key, as well as any nonstandardized key.