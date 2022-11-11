# OMF Instances
OMF Instances are a ZIP-based format to represent a portable Minecraft instance. OMF Instances are designed to be easily used by any launcher or modpack host.

OMF Instances MUST be a ZIP file and MUST contain a file named `instance.omf.json` (the [OMF Instance Index](#omf-instance-index)) within the root of the archive.

## OMF Instance Index (`instance.omf.json`)
The OMF Instance Index MUST be a UTF-8 encoded JSON file conforming to the following JSON properties.

### `formatType`
This property MUST be set to `instance`

### `formatVersion`
This property MUST be set to `0`. Future versions will increment this number.

### `project` (optional)
A [Project Metadata Reference](./Metadata_References.md#project-metadata-references) object for this instance.

### `version` (optional)
A [Version Metadata Reference](./Metadata_References.md#version-metadata-references) object for this instance's version.

### `assets` (optional)
An array of assets that should be downloaded, copied, or otherwise installed by an implementor. Each object within this array consists of the following properties.

#### `id`
A unique identifier for this asset. This SHOULD be consistent across multiple versions of the asset and multiple versions of the instance. For example, an asset of "MyMod" version 1.0 with ID `mymod` in instance version 1.0 should keep the same ID of `mymod` for "MyMod" version 2.0 and instance version 2.0.

#### `type`
An asset's `type` can be either:  

##### `remote`
This asset MUST be downloaded from a remote source, specified in the [`file`](#file) property. See the [`file`](#file) property documentation for more information about what is required.

##### `local`
This asset MUST be provided locally. Local files are found under the `local` folder in the instance archive, named after the asset's [`id`](#id). 

For example, if you have an asset with id `mymod`, the file `local/mymod` MUST exist within the archive root. Implementations MUST NOT attempt to add or guess file extensions - the file name MUST be exactly the same as the ID.

#### `file`
A [File Metadata Reference](./Metadata_References.md#file-metadata-references) object. However, this has a few required fields depending on the type of file and the type of asset.

The `type` field MUST always be present.

For assets of type `remote`, the `downloads`, `hashes`, and `size` fields MUST be present.

For assets of type `local`, neither `downloads`, `hashes`, nor `size` are required.

For files of type `raw`, the `dest` field MUST be present.

#### `project` (optional)
A [Project Metadata Reference](./Metadata_References.md#project-metadata-references) object for this asset.

#### `version` (optional)
A [Version Metadata Reference](./Metadata_References.md#version-metadata-references) object for this asset.

#### `groups` (optional)
An array of group IDs that this asset is a part of. See the [`groups` property in the Instance Index](#groups-optional-1) for more info.

#### `env`
Environments where this asset can be or must be installed. This property is an object consisting of both a `client` and `server` value, both of which MUST be present. Available values for `client` and `server` are `"required"`, `"optional"`, and `"disallowed"`. For example:

```json
"env": {
    "client": "required",
    "server": "optional"
}
```

Note that while clients technically have a logical server, the `server` property refers to the *dedicated* server only.

---

### `groups` (optional)
An array of different groups that may be selected by the user upon installation of the Instance. Each group is an object with the following properties.

#### `id`
A unique identifier for this group. This SHOULD be consistent across all versions of the Instance.

#### `name`
Human-readable name of this group.

#### `description` (optional)
A description to explain to the user the purposes of this group. It is RECOMMENDED that this is kept short.

#### `overrides` (optional)
The names of special overrides directories that will be applied to the Minecraft directory upon installation. See the [Group Overrides](#group-overrides) section for more info.

#### `env`
An environment specifier for this group, similar to [the one used for assets](#env). A group's `env` key is considered first, *before* an asset's `env` key. For example, in a group with:
```json
"env": {
    "client": "optional",
    "server": "disallowed"
}
```
and an asset with:
```json
"env": {
    "client": "required",
    "server": "disallowed"
}
```
the group's `optional` takes precedence over the asset's `required`. This means that the group itself is optional for clients, and if the group is selected by the user, the asset MUST be installed.

`optional` assets remain optional in a group, regardless of the group's `env` value. For example, in a group with:
```json
"env": {
    "client": "required",
    "server": "disallowed"
}
```
and an asset with:
```json
"env": {
    "client": "optional",
    "server": "disallowed"
}
```
The group itself MUST be enabled on clients, but the asset itself is optional. The user MUST be given the option to choose whether or not to install the asset.

When an `optional` asset is part of a group, it MUST NOT be able to be independently selected. Instead, the user MUST have to go through the groups that an asset is in.

The restriction on `server` only applying to dedicated servers applies here as it does to assets.

#### `requires` (optional)
A list of group IDs that this group requires MUST be enabled in order for it to be enabled.

#### `conflicts` (optional)
A list of group IDs that this group MUST NOT be allowed to be enabled alongside.

---

### `components`
A list of required components for implementations to use when installing this instance. This consists of mapping of unique IDs for components with their required versions.

The following component keys are allowed:
- `minecraft`: The Minecraft game
- `forge`: The Minecraft Forge modloader
- `fabric-loader`: The Fabric modloader
- `quilt-loader`: The Quilt modloader

Values are strings which specify an exact version of a component. For example:

```json
"components": {
    "minecraft": "1.18.2",
    "fabric-loader": "0.10.2"
}
```

### `config` (optional)
Configuration settings for launchers to use when installing this instance. Two properties are available: `ram` and `java`. Both are objects which consist of the optional `min` and `max` properties, which both apply inclusively. For example:

```json
"config": {
    "ram": {
        "min": 2,
        "max": 4,
    },
    "java": {
        "min": 8
    }
}
```
This instance requires at least 2 GB of RAM, but no more than 4. It also requires at least Java 8.

---

## File Format
OMF Instances are stored using the ZIP format and the `.omfinstance` extension. The correct media type to use when transferring over the internet is `application/x-omf-instance+zip`.

### Overrides
Overrides are directories stored in the root of the OMF Instance archive that contain files and directories that may be copied to the Minecraft root directory upon installation of the instance.

There are three base overrides directories: `overrides`, `client-overrides`, and `server-overrides`. The existence of each of these directories is optional.

`overrides` MUST be applied in all circumstances. `client-overrides` MUST be applied when an implementation is a client, and `server-overrides` MUST be applied when an implementation is a server. 

Note that while clients technically have a logical server, `server-overrides` MUST only be used for dedicated servers. Implementations CANNOT use `client-overrides` on a server or `server-overrides` on a client.

#### Group Overrides
Groups may also reference their own overrides directories, allowing for optional overrides. Therefore, overrides MUST be applied in the following order:
1. Common overrides (`overrides` directory)
2. Client or server overrides
3. All group overrides, sorted by the name of the overrides directory in ascending lexicograpical order by Unicode codepoint

All group overrides are applied with the prefix `overrides-`.

Any files that already exist when the next overrides layer is applied MUST be replaced by the newest layer's corresponding file.

See the following example on how to apply overrides for a client that has selected groups that use the overrides `1-custom-overrides` and `2-custom-overrides`.

The pack consists of this directory tree:
```
Example-Pack.omfinstance/
    overrides-1-custom-overrides/
        file.txt
    overrides-2-custom-overides/
        file.txt
    client-overrides/
        file.txt
        file2.txt
    server-overrides/
        server-only.txt
    overrides/
        file3.txt
    instance.omf.json
```
The applied directory will look like this directory tree:
```
.minecraft/
    file.txt
    file2.txt
    file3.txt
```
Note that the `file.txt` file MUST be the file in `overrides-2-custom-overrides`, as `2-custom-overrides` comes lexicographically after `1-custom-overrides`.

### Icon
Local instance icons may be provided inside the root of the archive via a file named `icon.apng`, `icon.gif`, or `icon.png`. Files MUST be preferred in that order, regardless of if other files exist. Instances are not required to have an icon.

Icons may be specified in the project metadata `icon` property. If an icon is provided locally in the archive, implementations MUST prefer it over the `icon` property. If a local icon does not exist, implementations MAY use the `icon` property.