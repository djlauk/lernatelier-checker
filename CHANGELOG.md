# Changelog
## [0.4.0] - 2026-06-19

### Bug Fixes
- Recognize lists with * and don't check for daily reflection ([`54b69d9`](https://github.com/djlauk/lernatelier-checker/commit/54b69d988c876071fa431f5c102d463d158d9c9f)) ([#1](https://github.com/djlauk/lernatelier-checker/issues/1))


### Refactoring
- Remove debug printout ([`278fb30`](https://github.com/djlauk/lernatelier-checker/commit/278fb30a509518792793ddc2ece3e3d3aab239c4))
- Use constants for checkbox regexes ([`433bc31`](https://github.com/djlauk/lernatelier-checker/commit/433bc31b2414969ac7c38a3eedf4bb86dc457d71))

**Full changelog:** [v0.3.0...v0.4.0](https://github.com/djlauk/lernatelier-checker/compare/v0.3.0...v0.4.0)
## [0.2.0] - 2026-06-16

### Build
- Add ruff linting and formatting ([`149d1cb`](https://github.com/djlauk/lernatelier-checker/commit/149d1cbb3a481b9c9f235b4fea1fab148b7a432c))


### Documentation
- Update README with --learning-period flag and config file format ([`9c236dd`](https://github.com/djlauk/lernatelier-checker/commit/9c236ddb4c429c164faa8ca3fe48c6439946ebd5))


### Features
- Per-day compliance tracking (days_ok / days_total) ([`6fdd7ad`](https://github.com/djlauk/lernatelier-checker/commit/6fdd7ad049b58f72530d0d1ec7394d7766cac936))
- Load lernperiode.json config for per-day and reflexion checks ([`7ed3a3a`](https://github.com/djlauk/lernatelier-checker/commit/7ed3a3aeabd6df9a74e4274c045c7e5171063a85)) ([#3](https://github.com/djlauk/lernatelier-checker/issues/3))
- Check if next school day is planned ([`5fe5637`](https://github.com/djlauk/lernatelier-checker/commit/5fe5637f41dd300ad41bab82e6f9bb092cac827b))

**Full changelog:** [v0.1.0...v0.2.0](https://github.com/djlauk/lernatelier-checker/compare/v0.1.0...v0.2.0)
## [0.1.0] - 2026-06-14

### Build
- Move dev deps to dependency-groups for seamless uv sync ([`2b89f7a`](https://github.com/djlauk/lernatelier-checker/commit/2b89f7a7446643581fe53e28bba05f6bb3f6c46f))
- Fix cliff template ([`fcd118d`](https://github.com/djlauk/lernatelier-checker/commit/fcd118dc6bbbf32afd770a99095386873aa8516d))


### Features
- Implement lernatelier-checker package ([`b67ebed`](https://github.com/djlauk/lernatelier-checker/commit/b67ebed9543be0d3ec1bff77f91e9872eb1c9e8a))
- Add PyInstaller exe build support ([`6107409`](https://github.com/djlauk/lernatelier-checker/commit/610740982f0b6f69c9ebdd0ddb3f89f6b864d9c5))
- Add --version flag ([`bdf10db`](https://github.com/djlauk/lernatelier-checker/commit/bdf10dbf02449f84e1eeb3aaccf771ccdf1cbf0e))


### Refactoring
- Split checks into sequence for easier understanding ([`15d8e0e`](https://github.com/djlauk/lernatelier-checker/commit/15d8e0e139c2466daa46ccdd640183ca40920a13))


