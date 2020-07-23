[![Python Version](https://img.shields.io/badge/python-3.8.3-blue?style=for-the-badge&logo=python)](https://www.python.org/downloads/release/python-383/) [![Quart Version](https://img.shields.io/badge/Quart-0.13.0-red?style=for-the-badge)](https://gitlab.com/pgjones/quart) [![Gino Version](https://img.shields.io/badge/Gino-1.1.0b1-blue?style=for-the-badge)](https://python-gino.org/) ![code style](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge)

<hr>

# Basho :house:

Basho (jap. room) is a quart application for room management with a user system and responsive material-style frontend. This is a rework of the basho with quart as new base.

## Installation

> This is not (yet) production ready

A working instance of [`pip`](https://packaging.python.org/tutorials/installing-packages/#installing-packages) and [python 3.8](https://www.python.org/downloads/release/python-382/) is required.

Install all dependencies:

`pip3 install -r requirements.txt`

Init git submodules (requires [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)):

`git submodule init`

Setup `.env` file (may vary for [windows](http://www.dowdandassociates.com/blog/content/howto-set-an-environment-variable-in-windows-command-line-and-registry/)) (Read by [dotenv](https://pypi.org/project/python-dotenv/)). Replace `{}` with your own credentials. `SECRET` should be e.g. a random generated string. `SECRET` is used as key for cookie encryption. See [Security](#Security) for more info.

```environment
DATABASE-USER={}
DATABASE={}
ADDRESS={}
PASSWORD={}
DEBUG={true is recommended}
DRIVER=postgres
SECRET={}
```

To use alembic for migrations you may need to change you `PYTHONPATH` according to [Gino and alembic](https://python-gino.org/docs/en/master/how-to/alembic.html#create-first-migration-revision). When using alembic you may need to change the auto generated files, if e.g. tables are deleted in an inappropriate order.

To apply the migrations you need to run `alembic upgrade head`.

Now your ready to run `python3 toolkit.py devserver` for a local [uvicorn](https://www.uvicorn.org/) development server. Run `python3 toolkit.py devserver --help` for further help and options.

The `toolkit.py` will also contain database utilities in the future.

## Development Notes

[Black](https://github.com/ambv/black) is used as code style. Consider using a black integration in your IDE.

## Frontend Design

Bootstrap 4 and MDBootstrap are used as frontend frameworks (See [attributions](#Attributions)). This also brings tooltips with popper.js and jquery as js frameworks. The areas of basho are differentiated by color accents. The application is generally in an `elegant` color (`#212121`) and takes advantage of `landing.jpg` as background. Layouts should take advantage of less than more. Make sure to test your layout on different devices ([firefox's](https://developer.mozilla.org/en-US/docs/Tools/Web_Console) & [chrome's](https://developers.google.com/web/tools/chrome-devtools/) dev console have a wonderful integration for this) for responsiveness.

| area           | color     |
| -------------- | --------- |
| auth           | primary   |
| admin          | danger    |
| rooms & events | secondary |

## Security

Security is handled by design with endpoint protection. The user system takes advantage of [`quart-auth`](https://pypi.org/project/quart-auth/).

> The `secret` must be kept _secret_. Change it to something secure (e.g. `python3 -c 'from secret import token_urlsafe; print(token_urlsafe())'`) and put it in your environment. _Don't hardcode it into the application_ It provides the encryption for [werkzeugs](https://pypi.org/project/Werkzeug/) secure session storage and cookies.

## Explanations

> Why are all css/ js/ icon libraries included locally instead via a cdn?

All external sources add a point of customer data processing when hitting the cdn. This may cause more work for the privacy policy in certain regions instead of only hitting your server. This also makes privacy related to e.g. logging of ip addresses an easier task to handle for sysops. This is part of this projects _privacy by design_ concept.

> Why quart and not flask

Cause it's faster and natively supports asnycio. I personally prefer async web development to synchronous web development if possible. Quart in particular can support the vast flask ecosystem and helped with the development.

## Attributions

- [Bootstrap 4](https://getbootstrap.com/) under [MIT License](https://github.com/twbs/bootstrap/blob/main/LICENSE)
- [Fontawesome 5](https://github.com/FortAwesome/Font-Awesome/blob/master/LICENSE.txt)
- [Jquery 3.5.1](https://jquery.org) under [MIT License](https://jquery.org/license/)
- [popper.js](https://popper.js.org/) under [MIT License](https://github.com/popperjs/popper-core/blob/master/LICENSE.md)
- [Material design for bootstrap 4 \(free\)](https://mdbootstrap.com/) under [MIT License](https://mdbootstrap.com/general/license/)
- All libraries mentioned in `requirements.txt`

## License

[MIT License by Cobalt](https://github.com/Chaostheorie/basho-reloaded/blob/master/LICENSE). This License applies to all the code created directly by Cobalt and doesn't apply to dependencies and included frameworks such as bootstrap 4 and jquery.

```text
MIT License

Copyright (c) 2020 Cobalt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Disclaimer

This application has no affiliation with [Basho Technologies](https://github.com/basho) and its name is based on the japanese word basho ~ room.
