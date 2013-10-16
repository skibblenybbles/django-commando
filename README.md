django-commando
===============

django-commando builds on Django's management command API to simplify writing,
overriding and sequencing Django management commands using a declarative style.

### Motivation

[Django](https://www.djangoproject.com/)'s management command API is the
everyday workhorse of the Django toolkit. However, the API is very basic
and doesn't provide convenient object-oriented hooks to modify the flow
of data and code through a command.

django-commando attempts to improve the management command API with the
following features:

*   a declarative API for managing and processing command options and
    option groups
*   a declarative API for specifying which action(s) to perform when
    the command is run
*   a uniform and relatively simple way to override existing management
    commands without writing nasty hacks
*   simple methods for checking the existence of and running other management
    commands and shell programs
*   optional overrides of Django's core and contrib management commands
*   optional overrides of management commands for the popular projects
    [South](http://south.aeracode.org/),
    [Haystack](http://haystacksearch.org/) and
    [django CMS](https://www.django-cms.org/en/)

### Installation

django-commando is published on [PyPI](https://pypi.python.org/pypi), so you
should install it with pip:

```
pip install django-commando
```

### Writing Management Commands

To write mangement commands, you'll need some familiarity with Python's
[`optparse`](http://docs.python.org/2/library/optparse.html) module
for creating and parsing command line options. It's assumed that you know
how to use the `optparse.make_option()` function.

You'll also need to understand the
[package structure for writing management commands](https://docs.djangoproject.com/en/1.5/howto/custom-management-commands/#module-django.core.management),
as documented by Django.

#### A simple development utility command: `searchcode`

To illustrate `commando`'s features, we'll write a simple management command
called `searchcode` that runs the shell program `grep` to search the current
directory for Python files containing a particular regular expression.

We'll start by creating a new app and setting up the proper package structure 
for the management command. Before we start, our project should have a layout
like this:

* `<project-root>`
    * manage.py
    * `<project>`
        * settings.py
        * wsgi.py
        * ...

Here, `<project-root>` is the root directory for your Django project,
`<project>` is the top-level package name for your project, and "..."
represents the various apps that you've written for your project.

Let's create a new `devutils` app by running:

```
$ python manage.py startapp devutils
```

We should also add `"<project>.devutils"` to our `INSTALLED_APPS` setting,
where `<project>` is the top-level package name for the project.

Under the new `devutils` app directory, we should now see:

* devutils
    * models.py
    * tests.py
    * views.py

We'll add `management` and `management.commands` packages under `devutils`, 
and we'll populate them with the modules that will implement the command:

* devutils
    * models.py
    * tests.py
    * views.py
    * management
        * \_\_init\_\_.py
        * searchcode.py
        * commands
            * \_\_init\_\_.py
            * seachcode.py

We'll define our command in `devutils.management.searchcode` and simply import it as
`Command` in `devutils.management.commands.searchcode`. Here's the definition of the
command in `devutils.management.searchcode`:

```python
from django.core.management import CommandError

from commando import management


class SearchCodeCommandOptions(management.CommandOptions):
    args = "[regular expression]"
    help = "Recursively search files under the current directory for a regular expression"
    option_list = ()
    option_groups = ()
    actions = ("searchcode",)
    
    def validate_searchcode(self, *arguments, **options):
        # Make sure this command was called with one argument.
        if not len(arguments) == 1:
            raise CommandError(
                "You must provide a regular expression")
        
        # Make sure grep is available in the shell.
        self.check_program("grep")
    
    def handle_searchcode(self, pattern, **options):
        self.call_program("grep", "-nrI", "--include=*.py", "-P", pattern, ".")


class SearchCodeCommand(SearchCodeCommandOptions, management.StandardCommand):
    option_list = management.StandardCommand.option_list
    option_groups = \
        SearchCodeCommandOptions.option_groups + \
        management.StandardCommand.option_groups
```

Then, in `devutils.management.comands.searchcode` we'll write:

```python
from ..searchcode import SearchCodeCommand as Command
```

Now, we should be able to run the command. From the `<project-root>` directory,
run this:

```
$ python manage.py searchcode "S.*Command"
./example/devutils/management/commands/searchcode.py:1:from ..searchcode import SearchCodeCommand as Command
./example/devutils/management/searchcode.py:6:class SearchCodeCommandOptions(management.CommandOptions):
./example/devutils/management/searchcode.py:26:class SearchCodeCommand(SearchCodeCommandOptions, management.StandardCommand):
./example/devutils/management/searchcode.py:27:    option_list = management.StandardCommand.option_list
./example/devutils/management/searchcode.py:29:        SearchCodeCommandOptions.option_groups + \
./example/devutils/management/searchcode.py:30:        management.StandardCommand.option_groups
```

You should see similar results for your project.

Now, let's look closely at the management command implementation in
`devutils.management.searchcode`. The definition is split up into two classes:
`SearchCodeCommandOptions`, which inherits from
`commando.management.CommandOptions` and `SearchCodeCommand`, which inherits
from the `SearchCodeCommandOptions` that we defined and from
`commando.management.StandardCommand`.

`SearchCodeCommandOptions` defines the options, options groups and actions that
are unique For the `searchcode` management command. `SearchCodeCommand` is the
actual command that will be run by Django. It uses multiple inheritance to mix
the functionality defined by `GruntCommandOptions` with the standard command
functionality defined by `commando.management.StandardCommand`.

You don't have to write two classes to create a management command, but
`commando`'s architecture encourages you to do so. By separating your command's
unique options and functionality into its own class, it will be easier to
override your command or add it to a command sequence implemented by another
management command.

The `SearchCodeCommandOptions` class defines several attributes and two
methods. The `args` and `help` attributes are used to populate the the message
that's displayed when `manage.py help searchcode` is run. The `option_list`
and `option_groups` attributes define the options that the command accepts.
We'll add some options shortly to improve our command and demonstrate this
feature.

When the command is invoked, its `handle()` method iterates over the names
in the `actions` attribute. It attempts to call a `validate_<action>()` method
for each action name. Then, it attempts to call a `handle_<action>()` method
for each action name. Since we've specified `("searchcode",)` for our `actions`
attribute, our `validate_searchcode()` and `handle_searchcode()` methods will
be run. Each will be called with a variable length list of arguments from the
command line and a dictionary of options, parsed by `optparse`.

Our `validate_searchcode()` method checks that exactly one argument has been
passed and raises `CommandError` otherwise. It also calls the helper method
`check_program` to verify that the `grep` command is available in the shell.

Since `validate_searchcode()` checked the number of arguments, the
`handle_searchcode()` method can safely accept a single argument of `pattern`,
instead of the more general `*arguments`, without risking a runtime
`TypeError`. The `handle_searchcode()` method invokes `grep` with the passed
pattern using the helper method `call_program()`. The `grep` call includes
the flags:

* `-n`: show line numbers
* `-r`: search files recursively
* `-I`: skip binary files
* `--include=*.py`: search only Python files
* `-P`: use Perl syntax for the regular expression




### Overriding Management Commands




### Sequencing Management Commands




### Utilities




### Included Management Command Overrides

django-commando provides management command overrides for Django,
South, Haystack and django CMS. Each of these commands improves the
`help` display and simply executes the underlying management command
when run.

To use the provided management command overrides, add any of the
`commando` apps shown below to the <em>end</em> of your `INSTALLED_APPS`
setting:

```python
INSTALLED_APPS = (
    # ...
    # Example apps that have commando.contrib overrides available.
    "cms",
    "haystack",
    "south",
    # ...
    # The management command overrides.
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

It's important that these management commands appear at the end of
`INSTALLED_APPS`. Django searches for management commands in the opposite
order of its other tools like template loaders and static files finders. It
will search the `INSTALLED_APPS` setting in reverse until it finds the
command. Here, `"commando.contrib.south"` appears below `"south"`, so 
when we run a `south` command, `commando`'s version in
`command.contrib.south` will be called.

Let's look at the `help` for `south`'s command `migrate`, which is handled
by `commando.contrib.south`:

```
$ python manage.py help migrate
Usage: manage.py migrate [appname] [migrationname|zero] [--all] [--list] [--skip] [--merge] [--no-initial-data] [--fake] [--db-dry-run] [--database=dbalias]

Runs migrations for all apps.

Options:
  -q, --quiet           Suppress all prompts and output.
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  [migrate options]:
    These options will be passed to migrate.

    --all               Run the specified migration for all apps.
    --list              List migrations noting those that have been applied
    --changes           List changes for migrations
    --skip              Will skip over out-of-order missing migrations
    --merge             Will run out-of-order missing migrations as they are -
                        no rollbacks.
    --no-initial-data   Skips loading initial data if specified.
    --fake              Pretends to do the migrations, but doesn't actually
                        execute them.
    --db-dry-run        Doesn't execute the SQL generated by the db methods,
                        and doesn't store a record that the migration(s)
                        occurred. Useful to test migrations before applying
                        them.
    --delete-ghost-migrations
                        Tells South to delete any 'ghost' migrations (ones in
                        the database but not on disk).
    --ignore-ghost-migrations
                        Tells South to ignore any 'ghost' migrations (ones in
                        the database but not on disk) and continue to apply
                        new migrations.
    --noinput           Tells Django to NOT prompt the user for input of any
                        kind.
    --database=DATABASE
                        Nominates a database to synchronize. Defaults to the
                        "default" database.

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

You can see that django-commando groups the options, showing you `migrate`'s
specific options, separated from the standard options for every Django command.
The `--version` and `-h, --help` options are added by the underlying
`optparse` module, and the `-q, --quiet` option is displayed at the top for
user convenience.

If we remove `"commando.contrib.south"` from `INSTALLED_APPS`, then `south`
will handle the `migrate` command:

```
$ python manage.py help migrate
Usage: manage.py migrate [options] [appname] [migrationname|zero] [--all] [--list] [--skip] [--merge] [--no-initial-data] [--fake] [--db-dry-run] [--database=dbalias]

Runs migrations for all apps.

Options:
  -v VERBOSITY, --verbosity=VERBOSITY
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings=SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath=PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Print traceback on exception
  --all                 Run the specified migration for all apps.
  --list                List migrations noting those that have been applied
  --changes             List changes for migrations
  --skip                Will skip over out-of-order missing migrations
  --merge               Will run out-of-order missing migrations as they are -
                        no rollbacks.
  --no-initial-data     Skips loading initial data if specified.
  --fake                Pretends to do the migrations, but doesn't actually
                        execute them.
  --db-dry-run          Doesn't execute the SQL generated by the db methods,
                        and doesn't store a record that the migration(s)
                        occurred. Useful to test migrations before applying
                        them.
  --delete-ghost-migrations
                        Tells South to delete any 'ghost' migrations (ones in
                        the database but not on disk).
  --ignore-ghost-migrations
                        Tells South to ignore any 'ghost' migrations (ones in
                        the database but not on disk) and continue to apply
                        new migrations.
  --noinput             Tells Django to NOT prompt the user for input of any
                        kind.
  --database=DATABASE   Nominates a database to synchronize. Defaults to the
                        "default" database.
  --version             show program's version number and exit
  -h, --help            show this help message and exit
```

For complex commands, you may find the option groups shown above helpful.
Each command overridden by `commando` groups the command's options for the
`help` display and calls the underlying management command when run. If you
don't care for the option grouping, don't add the `commando` apps to
`INSTALLED_APPS`.

If you include a `commando` app without the underlying app that it overrides,
the `help` message will inform you. For example, if we restore
`"commando.contrib.south"` and remove `"south"` in `INSTALLED_APPS`, we'll get
this:

```
$ python manage.py help migrate
Usage: manage.py migrate 

Unimplemented command.

Options:
  -q, --quiet           Suppress all prompts and output.
  --version             show program's version number and exit
  -h, --help            show this help message and exit

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

If we run such a command, we'll get an error:

```
$ python manage.py migrate
CommandError: This command is not implemented
```


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


