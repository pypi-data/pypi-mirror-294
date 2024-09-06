# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)[^1].

<!---
Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

-->

## [Unreleased]

## [1.0.1] - 2024-09-05

### Added

* New action to check the dependencies of a specific revision from a file's history.
* A message on top of the tracked dependency list indicates the number of unavailable dependencies.
* Utility actions on blocking and spline animation files to check the dependencies of the previous step, i.e. the latest revisions of layout and blocking files respectively.

## [1.0.0] - 2024-09-04

### Added

* Action to check all files linked into the latest revision of a Blender file, and download/request them when necessary.