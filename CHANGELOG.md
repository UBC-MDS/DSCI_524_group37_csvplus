# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] (Milestone 4) - 2026-02-02

### Fixed

- PR [#114](https://github.com/UBC-MDS/DSCI_524_group37_csvplus/pull/114) to reorganize `README.md` for clarity and usability for both users and developers to address peer review Issue [#103](https://github.com/UBC-MDS/DSCI_524_group37_csvplus/issues/103)
- PR [#121](https://github.com/UBC-MDS/DSCI_524_group37_csvplus/pull/121) to fix `resolve_string_value()` example in `README.md` to address peer review Issue [#100](https://github.com/UBC-MDS/DSCI_524_group37_csvplus/issues/100)
- Addressed inconsistencies in test_generate_report.py (#122)

### Added

- Retrospective and next steps to CONTRIBUTING.md (#126)

## [2.0.0] (Milestone 3) - 2026-01-25

### Added

- Additional unit tests for improved coverage (#95, #80)
- Flake8 linter to workflow (#83)
- Quartodoc YAML file for documentation (#91)
- Additional data validation and unit tests (#76)
- Deploy and build workflow files (#68, #71)

### Changed

- Bump package version from 0.1.2 to 0.2.2 (#97)
- Updated README for milestone 3 (#94)
- Updated dependencies and deleted commented out code (#62)
- Installed necessary dev and test dependencies (#69)

### Fixed

- Linter issues (#98)
- Action version and added skip-existing option (#96)
- Style issues and flake8 compliance (#89, #86)
- Docstring style errors (#73)
- Pandas version to pass all unit tests (#76)

## [1.0.0] (Milestone 2) - 2026-01-17

### Added

- Implemented `data_version_diff` function (#46)
- Created tests for `data_version_diff` function (#53)
- Improved test coverage for `data_version_diff` function (#56)
- Implemented `generate_report` function (#51)
- Implemented `load_optimized_csv` function with tests (#48)
- Implemented `resolve_string_value` function with unit tests (#40)
- Initial version of environment.yml (#32)

### Changed

- Updated README (#55)
- Updated docstring and function specs (#37)
- Renamed `data-correction.py` to `data_correction.py` and updated docstrings (#34)

## [0.0.1] (Milestone 1) - 2026-01-10

### Added

- Initial commit with project setup
- Function stub and docstring for `data_version_diff` (#17)
- Created `generate-report.py` with docstring (#15)
- Function definition and docstring for `load_optimized_csv` (#14)
- Added `resolve_string_value` function in data-correction.py (#13)
- Package details and contributors in README (#12)

### Changed

- Updated code of conduct to reflect group values (#11)
- Edited CONTRIBUTING.md (#18)
- Added raised errors to docstring (#16)

### Fixed

- Address inconsistencies in function names in README.md and data-correction.py (#21)
