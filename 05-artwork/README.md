# Artwork

Use the [artwork index](imported-artwork-index.md) to find and catalog visual material. The [visual style and character prompts](visual-style-and-character-prompts.md) document the current provisional direction. Store full-resolution source files in the category that matches their primary use.

| Category | What goes here |
| --- | --- |
| [Concept art](concept-art/) | Versioned character portraits and prompts, plus explorations of environments, objects, and visual tone. |
| [Habitat diagrams](habitat-diagrams/) | Layouts, cutaways, and schematics for habitat spaces and systems. |
| [Character references](character-references/) | Reference sheets and visual studies for named characters. |
| [Maps](maps/) | Geographic, orbital, and route maps. |
| [Story diagrams](story-diagrams/) | Plot, scene, and causality diagrams. |
| [Other visual material](other-visuals/) | Mood boards and references that fit none of the other categories. |

## Adding artwork and versions

1. Save the original at its native resolution and in its original format. Preserve the original filenames and paths of archived imports.
2. For new work, use an asset family and a version suffix, such as `asset-name-v01.png` and `asset-name-v02.png`. Keep each version in its own file and retain the earlier versions. Check that a filename is free before saving. Treat a crop, annotation, or smaller export as a separate derivative and link it to the original.
3. Add one row per file to the index. Record its intended use, canon status, creation date when known, provenance, and related material. Cite the previous version or source image in the source notes. Record a tool, model, prompt, or usage rights when available. Use **Unknown** for missing evidence and keep archive packaging dates distinct from creation dates.
4. Mark new story visuals **PROVISIONAL** while their story details await approval. Use **OPEN QUESTION** when a visual is specifically intended to solicit an unresolved decision. Use **LOCKED CANON** only for details explicitly approved by the author and recorded in the Story Bible. Link to the approved entry and specify which visual details it covers. [Canon approval workflow](../AGENTS.md#propose-review-and-apply-changes)

See the [character concept workflow](concept-art/README.md#character-concepts) for keeping each profile’s current portrait and prompt in sync.

## Git LFS assessment

The current full-resolution character concepts are each under 3 MiB. Regular Git is a good fit at this scale. [GitHub file limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)

Revisit LFS if the project starts retaining many large binary versions or layered working files. LFS keeps small pointers in Git history and stores the binaries separately, which can reduce the amount of history fetched during a clone. Collaborators need Git LFS and access to its object store to retrieve the originals, and storage and downloads count toward separate GitHub LFS quotas. Existing Git history retains blobs already committed unless it is rewritten. If adoption becomes useful, scope it to future large assets and obtain approval before enabling it. [GitHub LFS overview](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
