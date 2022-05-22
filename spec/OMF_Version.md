# OMF Versions
OMF Versions are a metadata format to provide information about a specific version of a Project. They have the following properties:

## `formatType`
This MUST be set to `omf:version`

## `formatVersion`
This MUST be set to `0`. Future versions will increment this number.

## `meta` (optional)
A [Combined Metadata Reference](./Metadata_References.md#combined-metadata-references) object. Allows you to specify Version name, components, dependencies, changelog, and more, as well as information about the parent Project.

## `files`
A list of files for this Version. There are 3 available types of files specified via the `fileType` property: `raw`, `jarmod` and `versionJson`

### `versionJson` file type
This represents a Mojang Version JSON file to be applied, usually as a custom mod loader. [See more in the OMF Pack specification](./OMF_Pack.md#file-type-versionjson)

## `jarmod` file type
This represents a legacy JAR mod, to be copied into the Minecraft JAR. [See more in the OMF Pack specification](./OMF_Pack.md#file-type-jarmod)

## `raw` file type
This represents a simple file to be placed somewhere in the Minecraft instance directory. This adds one additional field, that being `fileName`, which is the name of the file that is being downloaded.

**All file types share the following properties:**

### `primary` (optional)
A boolean value indicating whether or not this is the primary file.

### `downloads`
An array of URLs providing this file. Implementations MUST download these in order from first to last.

### `hashes`
An object consisting of hashes for this file. Available hashes are `sha1` and `sha512`. For example:
```json
"hashes": {
    "sha1": "< SHA1 sum >",
    "sha512": "< SHA512 sum >"
}
```

Implementations MUST check downloaded files against these hashes

### `fileSize`
The size of this file, in bytes.