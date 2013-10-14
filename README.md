django-commando
===============

django-commando builds on Django's management command API to simplify writing,
overriding and sequencing Django management commands in a declarative style.

### Motivation

[Django](https://www.djangoproject.com/)'s management command API is the
everyday workhorse of the Django toolkit. However, the API is very basic
and doesn't provide convenient object-oriented hooks to modify the flow
of data and code through a command.

django-commando attempts to improve the management command API with the
following features:

*   a declarative API for managing and processing command options and
    option groups
*   a declarative API for specifying which action or actions to perform when
    the command is run
*   a uniform and relatively simple way to override existing management
    commands without writing nasty hacks
*   simple methods for checking the existence of and running other management
    commands and shell programs
*   optional overrides of Django's core and contrib management commands
*   optional overrides of management commands for the popular projects
    [South](http://south.aeracode.org/),
    [django-haystack](http://haystacksearch.org/) and
    [django-cms](https://www.django-cms.org/en/)

### Installation and Usage

django-commando is available on PyPI, so you should install it with pip:

```
pip install django-commando
```

To use the provided Django or third-party management command overrides,
add any of these to the <em>end</em> of your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = (
    # ...
    # Example apps that have commando.contrib modules available.
    "cms",
    "haystack",
    "south",
    # ...
    # # The commando management command override apps.
    "commando.django.core",
    "commando.django.contrib.auth",
    "commando.django.contrib.gis",
    "commando.django.contrib.sessions",
    "commando.django.contrib.sitemaps",
    "commando.django.contrib.staticfiles",
    "commando.contrib.cms",
    "commando.contrib.haystack",
    "commando.contrib.south",
)
```

To see it in action, let's look at the `help` output for the 
`runserver` command:

```
$ ./manage.py help runserver
Usage: manage.py runserver [optional port number, or ipaddr:port]

Starts a lightweight Web server for development and also serves static files.

Options:
  -q, --quiet           Suppress all prompts and output.
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  [runserver options]:
    These options will be passed to runserver.

    -6, --ipv6          Tells Django to use a IPv6 address.
    --nothreading       Tells Django to NOT use threading.
    --noreload          Tells Django to NOT use the auto-reloader.
    --nostatic          Tells Django to NOT automatically serve static files
                        at STATIC_URL.
    --insecure          Allows serving static files even if DEBUG is False.

  [standard options]:
    Standard Django management command options.

    -v VERBOSITY, --verbosity=VERBOSITY
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
    --settings=SETTINGS
                        The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
    --pythonpath=PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
    --traceback         Print traceback on exception
```

You can see that django-commando groups the options, showing you `runserver`'s
specific options, separated from the standard options for every Django command.
The `-q, --quiet`, `--version` and `-h, --help` options are kept at the top
for user convenience.

django-commando's command overrides implement option grouping like this. Under
the hood, they defer to the underlying active command, so for this configuration,
when you run the `runserver` command, the underlying
`django.contrib.staticfiles.management.commands.runserver.Command` command
is run.

django-commando provides base classes for writing, overriding and sequencing
management commands. Read on to see how to use them.


### Writing Management Commands


### Overriding Management Commands


### Sequencing Management Commands


### Utilities


### Included Management Command Overrides


#### `commando.django.core`


#### `commando.django.contrib.auth`


#### `commando.django.contrib.gis`


#### `commando.django.contrib.sessions`


#### `commando.django.contrib.sitemaps`


#### `commando.django.contrib.staticfiles`


#### `commando.contrib.cms`


#### `commando.contrib.haystack`


#### `commando.contrib.south`


### Notes


