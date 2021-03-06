# Inkblot

**Note: This is a super early prototype might-not-have-time-energy-to-finish-it project.  Probably don't use it.**

Generate your static site.

## Roadmap

  1. ~~Nested directories.~~
  2. ~~Layouts~~
  3. ~~Includes/underscore files~~
  4. ~~Config~~
  5. ~~Styling/Sass~~
  6. ~~Static files/images?~~
  7. ~~CLI~~
  8. Object model?  Like specify "things" with fields that have default pages/display styles?
  9. Extend that to Posts and Tags at least as the basic "things" supported out of the box.
  10. Plugins
  11. Moar Configuration.
  12. Enable auto-reloading by keeping track of modification time

## Ideas

- Configure sass/scss output style in config?
- Figure out how to do relative pathing for includes?
- There's room for more fancy static file specification (specific files or directories or patterns), but right now, it works by any non-recognized file extension being considered a static file.  And at least now it handles binary files smoothly as well.
- Dev server doesn't reload/find newly created files?

## Contributing

It's early yet, but I'd love contributers!

1. Clone and enter the repo.

```bash
git clone git@github.com:rpalo/inkblot.git
cd inkblot
```

2. Create a virtual environment and activate it (activation must be done every time before working on it).

```bash
python3 -m venv .venv

# In Bash
source .venv/bin/activate
# PowerShell
.venv/Scripts/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
pip install -e .
```

And you're ready to go.  To test things out on the example directory, run:

```bash
inkblot build -d example
```

It should build and be amazing.
