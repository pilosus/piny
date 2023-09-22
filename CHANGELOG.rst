Changelog
---------

v1.1.0 (2023-09-22)
...................

* Added: new validator `PydanticV2Validator` to support Pydantic v2


v1.0.2 (2023-02-03)
...................

* Update GitHub workflow for CI: run tests & license checks for PRs, pushes to master and tags (#202) by @pilosus
* Make dependabot update GitHub Actions (#202) by @pilosus


v1.0.1 (2023-02-03)
...................

* Run tests against locally installed package instead of using ugly imports (#200) by @pilosus

v1.0.0 (2023-01-02)
......................

See release notes to `v1.0.0rc1`

v1.0.0rc1 (2023-01-01)
......................

**Release breaks backward compatibility!**

* Bump major dependencies: `PyYAML>=6,<7` `Click>=8,<9` (#192) by @pilosus
* `Marshmallow` integration supports only v3.0.0 and later (#192) by @pilosus
* Move to `pyproject.toml` for packaging (#193) by @pilosus
* Raise Python requirement to `>=3.7` (#193) by @pilosus

v0.6.0 (2019-06-27)
...................
* Add CLI utility (#35) by @pilosus
* Update documentation, add integration examples (#34) by @pilosus

v0.5.2 (2019-06-17)
...................
* Fix ``Help`` section in ``README.rst`` (#31) by @pilosus
* Fix Sphinx release variable (#30) by @pilosus

v0.5.1 (2019-06-17)
...................
* Fix Sphinx config, fix README.rst image markup (#28) by @pilosus

v0.5.0 (2019-06-17)
...................
* Sphinx documentation added (#12) by @pilosus
* Piny artwork added (#6) by Daria Runenkova and @pilosus

v0.4.2 (2019-06-17)
...................
* Rename parent exception ``PinyError`` to ``ConfigError`` (#18) by @pilosus
* Add feature request template for GitHub Issues (#20) by @pilosus

v0.4.1 (2019-06-17)
...................
* Issue and PR templates added, minor docs fixes (#16) by @pilosus

v0.4.0 (2019-06-16)
...................
* Data validators support added for ``Pydantic``, ``Marshmallow`` (#2) by @pilosus
* ``CONTRIBUTING.rst`` added (#4) by @pilosus

v0.3.1 (2019-06-09)
...................
* Minor RST syntax fix in README.rst (#9) by @pilosus

v0.3.0 (2019-06-09)
...................
* README.rst extended with ``Rationale`` and ``Best practices`` sections (#5) by @pilosus

v0.2.0 (2019-06-09)
...................
* StrictMatcher added (#3) by @pilosus

v0.1.1 (2019-06-07)
...................
* CI/CD config minor tweaks
* README updated

v0.1.0 (2019-06-07)
...................
* YamlLoader added
* Makefile added
* CI/CD minimal pipeline added

v0.0.1 (2019-06-07)
...................
* Start the project
