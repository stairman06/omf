# OMF Components
OMF Components are standard format to define a Minecraft "component". Components consist of libraries, JVM and Minecraft arguments, Java main classes, and Java agents. Launchers can use components to allow users to install different modloaders, without the launcher needing to add custom support.

## Component Files
OMF Component files MUST be a UTF-8 JSON file. Component file names MAY end in either `.omf.json` or `.omfcomponent`. Each file MUST conform to the following JSON properties.

### `formatType`
MUST be set to `component`

### `formatVersion`
MUST be set to `0`. Future versions will increment this number.

### `project` (optional)
A [`Project Metadata Reference`](./Metadata_References.md#project-metadata-references) for this component.

### `version` (optional)
A [`Version Metadata Reference`](./Metadata_References.md#version-metadata-references) for this component.

### `arguments` (optional)
An object consisting of a `jvm` key, which defines additional arguments for the JVM, and a `game` key, which defines additional arguments for Minecraft.

Both `jvm` and `game` are an object consisting of three properties, `client`, `common`, and `server`, each of which have an array value. Each array consists of [`Mojang Arguments`](#mojang-arguments).

Implementations should use the JVM and Minecraft arguments for their side (e.g. `client` or `server`) as well as arguments within `common`. Note that Mojang arguments may have special conditions that determine whether or not the individual argument should be applied.

### `libraries` (optional)
An object consisting of three properties, `client`, `common`, and `server`, each of which have an array value. Each array consists of [`Mojang Maven Library Definitions`](#mojang-maven-library-definitions).

Implementations should download and include in the classpath libraries from their side (e.g. `client` or `server`) as well as libraries within `common`.

### `agents` (optional)
An object consisting of three properties, `client`, `common`, and `server`, each of which have an array value. Each array consists of [`Mojang Maven Library Definitions`](#mojang-maven-library-definitions).

Implementations should download and append an argument to the JVM adding the library as a Java agent, using the `-javaagent` JVM argument. Implementations should use agents from their side (e.g. `client` or `server`) as well as agents within `common`.

### `mainClass` (optional)
An object consisting of a `client` and `server` value. Both specify the Java main class that should be used when launching for their side.

---

## Mojang Maven Library Definitions
A library object from Mojang's [version JSON files](https://minecraft.fandom.com/wiki/Client.json). More documentation will be added later.

## Mojang Arguments
An argument object from Mojang's [version JSON files](https://minecraft.fandom.com/wiki/Client.json). More documentation will be added later.

## Inspiration
OMF Components are inspired by MultiMC and Prism Launcher's components. Sidedness is inspired by Fabric Meta's `launcherMeta` property.

## Implementation Suggestions
Components have great potential to cause harm!