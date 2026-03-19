# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-03-19

### Added
- **Aesthetics**: New ASCII banner and ANSI color support for a premium CLI experience.
- **Progress Bar**: Real-time visual feedback for both uploads and downloads.
- **Cross-Platform**: Full support for **macOS** and **Windows** (including `install.bat`).
- **Default Provider**: Integrated **Litterbox (Catbox.moe)** as the default reliable storage provider.
- **Custom Relays**: Ability to use self-hosted relay servers via `--relay-url`.
- **Improved UX**: The `send` command now automatically generates the exact `receive` command for the recipient.

### Changed
- Updated default storage provider to Litterbox for better reliability.
- Modernized packaging using `pyproject.toml`.

## [1.0.0] - 2026-03-18

### Added
- Initial release.
- Core encryption engine using **AES-256-GCM**.
- Support for `file.io` and `pixeldrain` providers.
- Basic `send` and `receive` CLI commands.
