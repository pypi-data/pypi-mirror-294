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

## [1.1.1] - 2024-09-06

### Added

* When building an animation blocking scene, the resulting file is left empty until building is done, or in case it encounters an error.

## [1.1.0] - 2024-09-05

### Added

* New action to build a compositing scene from a spline animation scene.
* Handling of compositing scene building errors by filtering the subprocesses outputs. Filters are defined in the project settings (*Runner Error Handlers*).

## [1.0.3] - 2024-05-29

### Fixed

* Layout and blocking files are created with the path format of their corresponding presets in the task manager (when defined).

### Added

* New action to build a Blender blocking scene.

## [1.0.2] - 2024-05-21

### Added

* An option to refresh dependencies (which might be updated in Kitsu before the cache invalidates).

## [1.0.1] - 2024-05-16

### Changed

* A layout scene is now built with the video of the animatic (in addition to its audio track), using the updated LFS Playblast `scene_builder_add_animatic` operator.

## [1.0.0] - 2024-05-16

### Added

* initial release
