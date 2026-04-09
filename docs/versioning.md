# Standards Versioning

This repository is versioned independently from consumer repositories.

## Version model

- `MAJOR`: breaking policy/template changes requiring migration.
- `MINOR`: backward-compatible additions and improvements.
- `PATCH`: fixes, clarifications, typo/docs fixes.

## Recommended consumer workflow

1. Pin a standards version in a `STANDARDS_VERSION` file.
2. Upgrade intentionally (for example, quarterly).
3. Read migration notes before applying new baseline changes.

## Release notes

Each release should include:

- changed templates/files;
- migration impact;
- required consumer actions.
