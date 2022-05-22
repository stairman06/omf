# OMF Packs 
OMF Packs are a ZIP-based format to represent a Minecraft pack. OMF Packs MUST be stored as a ZIP file and MUST contain a file named `index.omf.json`, which is the OMF Pack Index, at the root of the archive.

## OMF Pack Index (`index.omf.json`)
The OMF Pack Index file MUST be a UTF-8 encoded JSON file conforming to the following JSON properties

### `formatType`
This property MUST be set to `omf:pack`

### `formatVersion`
This property MUST be set to `0`. Future versions will increment this number.

### `components`
A list of required components for implementations to use when attempting to install this Pack. This property consists of a key-value mapping, with keys representing a unique ID for the component, and the value representing the version of the component.

The following component keys are allowed:
- `minecraft`: The Minecraft game
- `forge`: The Minecraft Forge mod loader
- `fabric-loader`: The Fabric mod loader
- `quilt-loader`: The Quilt mod loader

Values are strings which specify an exact version of the component. For example:

```jsonc
"components": {
    "minecraft": "1.18.2",
    "fabric-loader": "0.10.2"
}
```

`fabric-loader` and `quilt-loader` are both fully representable as files with the `versionJson` type. However, whenever either of those are used, they MUST be used as components. 

### `files`
A list of files for this Pack that may need to be downloaded. Each entry in this array consists of the following. There are 3 types of files, as specified by the `fileType` property: `jarmod`, `versionJson` and `raw`.

#### File type `jarmod`
Jar mods are a legacy form of Minecraft mods that involve placing files directly into the Minecraft game jar. `jarmod` files are packaged as ZIPs and must be extracted directly into the Minecraft jar. For example, if you downloaded the file `my-jarmod.zip`:

```
my-jarmod.zip/
    a.class
    b.class
```
The files `a.class` and `b.class` inside the Minecraft jar MUST be overwritten with the replacement files.

Implementations SHOULD also automatically delete the META-INF directory inside the Minecraft game jar to allow the game to properly launch.

#### File type `versionJson`
Version JSONs (also referred to as `client.json` by [the Minecraft Wiki](https://minecraft.fandom.com/wiki/Client.json)), are instructions to a launcher on how to launch the game.

TODO: More implementation details will be added later.

#### File type `raw`
This is a file that must simply be placed into a directory relative to the Minecraft instance. 

This consists of one additional property, `path`, which is the destination of the file, relative to the Minecraft instance directory. For example, `mods/mymod.jar` resolves to `.minecraft/mods/mymod.jar`. Implementations SHOULD implement precautions to prevent escaping the Minecraft instance directory.

**All file types share common properties, which are listed below**

#### `id`
A unique identifier for this file. This MUST remain identical across vresions of the Pack for the same file or mod.

#### `downloads`
An array of URLs where this file may be downloaded. Files MUST be downloaded in order, from first to last. Implementations should continue downloading until a file with a valid hash has been found, or all URLs have been used.

#### `local`
A path to a file, relative to a directory named `local` inside the .omfpack file, where this file may be obtained. This allows files to be shipped directly with the pack, and to be also fully-optional and to support version JSONs and jarmods.

For example, a file with `"local": "my-jarmod.zip"` and the following directory structure:
```
modpack.omfpack/
    overrides/
    local/
        my-jarmod.zip
    index.omf.json
```

The file `local/myjarmod.zip` MAY be used. 

Note that at least `downloads` or `local` MUST be provided in a file to be considered valid. Both may also be provided. Implementation MAY prioritize `downloads` or `local` - there is no requirement.

#### `hashes`
An object consisting of hashes of this file. The following hashing methods are available:
- `sha1`
- `sha256`
- `sha512`

See the following example:
```jsonc
"hashes": {
    "sha1": "< SHA1 sum >",
    "sha512": "< SHA512 sum >"
}
```

At least one hash MUST be provided. Implementations SHOULD implement all hashes.

#### `fileSize`
The size of this file in bytes. Implementations SHOULD use this to display download progress to the user.

#### `groups` (optional)
A list of Group IDs to allow users to select which set of files they would like to download. See the [groups key section](#Groups) for more info.

#### `env` (optional)
For files that are either optional or allowed in specific environments, this property allows such to be defined. This property is an object consisting of both a `client` and `server` values, both of which MUST be present, however the `env` key itself is optional. For example:

```jsonc
"env": {
    "client": "required",
    "server": "optional"
}
```
Available values are `required`, `optional` and `disallowed`. 

Note that while client technically have a logical server, the `server` property refers to the *dedicated* server only.

#### `meta` (optional)
A [Combined Metadata Reference](./Metadata_References.md#combined-metadata-references) object for this file.

---

### `groups` (optional)
A mapping of Group IDs to Group Definition objects. Group IDs MUST remain the same across all versions of a Pack. Group Definition objects consist of the following properties:

#### `name`
The human-readable name of this Group.

#### `description` (optional)
A short description to explain this Group.

#### `overrides` (optional)
The name of a special overrides directory that will be applied to the Minecraft instance upon Pack installation. See [Overrides](#Overrides) for more info.

#### `env` (optional)
An environment specifier for this Group, similar to [the one used for files](#env-optional). The Group `env` key acts as a "filter" for the files in the Group. For example, in a Group with:
```jsonc
"env": {
    "client": "required",
    "server": "disallowed"
}
```
and a file with
```jsonc
"env": {
    "client": "optional",
    "server": "disallowed"
}
```
the Group itself MUST be enabled, allowing other properties such as `overrides` to apply. However, any optional file corresponding to the group MUST be able to be chosen by the user as they please.

The restriction on the `server` property applying to only dedicated servers applies to here as it does to a file's `env`.

#### `requires` (optional)
A list of Group IDs that this Group requires MUST be enabled for this Group to be enabled.

#### `conflicts` (optional)
A list of Group IDs that this Group MUST NOT be allowed to be enabled alongside.

---

### `meta` (optional)
A [Combined Metadata Reference](./Metadata_References.md#combined-metadata-references) object for this Pack.

### `config` (optional)
Configuration settings for launchers to use when importing this Pack. Two properties are available: `ram` and `java`. Both are objects which consist of the optional `min` and `max` properties, which apply inclusively. For example:

```json
"config": {
    "ram": {
        "min": 2,
        "max": 4
    },
    "java": {
        "min": 8
    }
}
```

---

## File Format
OMF Packs are stored using the ZIP format and the `.omfpack` extension. The correct media type to use when transferring over the internet is `application/omf-pack+zip`.

### Overrides
Overrides are directories stored in the root of the OMF Pack file that contain files and directories that may be copied upon installation of the Pack. 

There are three base overrides directories: `overrides`, `client-overrides`, and `server-overrides`. The existence of each of these directories is optional. `overrides` MUST be applied in all circumstances. `client-overrides` MUST be applied when an implementation is a client, and `server-overrides` MUST be applied when an implementation is a server. Implementations MUST NOT apply both client and server overrides.

Note that while clients do technically have a logical server, `server-overrides` as well as the `server` property in `env` objects only applies to a dedicated server.

Groups may also reference their own overrides directories, allowing for optional and sided overrides. Therefore, overrides MUST be applied in the following order:
1. Common overrides (`overrides` directory)
2. Client or server overrides
3. All Group overrides, sorted in ascending lexographic order by Unicode codepoint

Any files that already exist when the next overrides layer is applied MUST be replaced by the newest layer's corresponding file.

See the following example on how to apply overrides for a client that has selected Groups that use the overrides `1-custom-overrides` and `2-custom-overrides`.

The pack consists of this directory tree:
```
example_pack.omfpack/
    1-custom-overrides/
        file.txt
    2-custom-overrides/
        file.txt
    client-overrides/
        file.txt
        file2.txt
    server-overrides/
        server-only.txt
    overrides/
        file3.txt
    index.omf.json
```
The applied directory will look like this directory tree:
```
.minecraft/
    file.txt
    file2.txt
    file3.txt
```
Note that the `file.txt` file MUST be the file in `2-custom-overrides`, as `2-custom-overrides` comes lexicographically after `1-custom-overrides`.
