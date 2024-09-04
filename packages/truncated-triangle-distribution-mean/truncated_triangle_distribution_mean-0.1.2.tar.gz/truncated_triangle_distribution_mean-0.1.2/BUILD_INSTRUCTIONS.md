# Steps to build a new version

Since this is a small personal project that I don't forsee updating often, I haven't had a need to utilise github actions to their full potential and do this all automatically yet. The current release process is:

1. Update version in `pyproject.toml`.
2. Build with `python -m build`
3. Upload distributions with: `python -m twine upload dist/*`
4. Create a tag on the main branch with: `git tag x.y.z`.
5. Push tag with: `git push origin tag x.y.z`.
