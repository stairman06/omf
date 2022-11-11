# Metadata References
Metadata References are used through the OMF standard to allow standardized and non-standardized metadata to be referenced.

Any nonstandard properties MUST be prefixed with `x-`. 

### Project Metadata References
Project Metadata References refer to a project. They consist of the following properties. Note that all fields are optional unless otherwise mentioned.

#### `id`
A globally-unique identifier for this project. It is RECOMMENDED that this is something provably-unique, such as a reverse domain name identifier. However, there are no restrictions on what this can be.

#### `src`
URL where the full OMF Project Metadata can be found.

#### `name`
Human-readable name of the project.

#### `summary`
A summary of the project. RECOMMENDED to be short.

#### `icon`
URL to an icon representing the project. RECOMMENDED to be a square PNG, APNG, GIF, or JPEG image. 

#### `releaseDate`
An ISO 8601 string representing the initial release date of the project.

### Version Metadata References
Version Metadata References refer to a specific version of a project. They consist of the following properties. Note that all fields are optional unless otherwise mentioned.

#### `id`
A project-level unique identifier for this version. There are no restrictions on this field. It SHOULD be unique to the project.

#### `src`
URL where the full OMF Version Metadata can be found.

#### `name`
Human-readable name of the version.

#### `semver`
A [Semantic Versioning](https://semver.org/) number for this version. Do not use this field unless your project is guaranteed to follow SemVer for all future versions.

#### `releaseDate`
An ISO 8601 string representing the release date of the version.

#### `components`
An OR set of required components for this version. Each object contained in this array is one possible configuration that may be required when using this versino. For example:
Available components are `minecraft`, `fabric-loader`, `forge`, and `quilt-loader`. Each component corresponds to a specifier for which versions are considered valid.

Specifiers can be:
- Literal strings: this exact version MUST be installed
- Arrays: one of these versions MUST be installed. Each item in this array MUST be a literal string. For example, you cannot have `["1.17", ">=1.18.2"]`
- Inequalities: prefixed with either `>=` or `<=`. The version after the prefix is either the minimum or the maximum. 
- All versions: an asterisk can be used to allow all versions

Example:
```json
"components": [
    {
        "minecraft": "1.18.2",
        "forge": "*"
    },
    {
        "minecraft": ["1.18.2", "1.18.1", "1.18"],
        "fabric-loader": ">=0.10.2"
    }
]
```

In the above example, the version can be installed to Minecraft 1.18.2 with any version of Forge. Or, it can be installed to Minecraft 1.18.2, 1.18.1, or 1.18 with at least Fabric 0.10.2

Note that this is an OR array, and as such, multiple configurations can be matched. However, one MUST be matched in order to allow installation.

#### `relations`
A list of projects and/or versions related to this one.  Each relation has a specified `type` as well as `project` and `version` metadata. Available types are `requires`, `conflicts`, `recommends`, and `embeds`. For example:
```json
"relations": [
    {
        "type": "requires",
        "project": {
            "id": "com.example.Library",
            "name": "Required Library"
        },
        "version": {
            "releaseDate": "2022-01-01T00:00:00Z"
        }
    },
    {
        "type": "conflicts",
        "project": {
            "id": "com.example.Library",
        },
        "version": {
            "releaseDate": "2022-01-02T00:00:00Z"
        }
    }
]
```
This example requires a version of "Required Library" released anytime after `2022-01-01T00:00:00Z`. However, it conflicts with versions released after `2022-01-02T00:00:00Z`. Therefore, in order for a required version to be considered valid, it MUST fall within those two ranges.

Version comparison for `required` and `conflicts` is a tricky thing as there is no standard used across all mods. Therefore, implementors MUST use the fallback system described here. Implementors MUST compare versions using the following order:
1. **Exact properties.** These are properties which are exactly the same on both ends. Applies to `id` and `src`. Implementors MUST NOT apply this to fields such as `name` which are not guaranteed to be consistent.
2. **Validation properties.** These are properties which can be directly validated using a standard formula when present on both ends. Applies to `semver`.
3. **Minimum properties.** These are properties where the supplied value in the relationship object acts as a minimum. Applies to `releaseDate`.

When following this order, implementations MUST short-circuit if one of the properties matches. For example, if mod Foo requires Bar with version ID `1.0`, and that is already installed, the implementation should terminate immediately as the version `id`s match exactly.

In order to match a specified project, it is RECOMMENDED to use fields such as `id`, `src` or `name`. There is no required pattern for this that implementations must follow.

### File Metadata References
File Metadata References refer to a specific file of a version. They consist of the following properties. Note that all fields are optional unless otherwise mentioned.

#### `primary` (optional)
Whether or not this is the primary file. This is only used in an [OMF Version](./OMF_Version.md)'s file listing. Only one file can be allowed primary, but implementors MUST prefer the first `primary` file if there are multiple.

This field MAY be omitted from [OMF Version](./OMF_Version.md) file listings. If not present, it will equate to `false`. 

This field has no significance when used in an [OMF Instance](./OMF_Instance.md).

#### `type`
The type of this file. The following values are available:
- `raw`: this file must simply be placed within the Minecraft directory. Requires [`dest`](#dest-only-for-type-of-raw).
- `jarmod`: a jarmod that should be extracted within the Minecraft client jar.
- `versionJson`: a Mojang version JSON file specifying custom libraries, classes, etc.
- `instance`: an [OMF Instance](./OMF_Instance.md)

#### `dest` (only for `type` of `raw`)
Only allowed when `type` is `raw`. Implementors SHOULD ignore it if present for versions other than `raw`. Specifies the path within the Minecraft instance directory that this file should be placed. For example, a `dest` of `mods/mymod.jar` should be placed within `.minecraft/mods/mymod.jar`.

Implementors SHOULD take measures to prevent files from escaping the Minecraft directory.

#### `downloads`
A list of URLs where this file can be downloaded. If present, requires `hashes`.

#### `hashes`
An object consisting of checksums of the file. Each key is a hash function, with the corresponding hexadecimal output as the value. Available keys are `sha1`, `sha256`, and `sha512`.

Nonstandard hashing methods MAY be used, but at least one of the above hashing method MUST be provided. 

#### `size`
The size of this file, in bytes.