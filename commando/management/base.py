import collections
import optparse
import os
import subprocess

from django.core import management
from django.utils.importlib import import_module

from functools import reduce


def get_option_default(option):
    """
    Given an optparse.Option, returns a two-tuple of the option's variable name
    and default value.
    
    """
    return (
        option.dest, 
        None if option.default is optparse.NO_DEFAULT else option.default,
    )


def get_option_defaults(command):
    """
    Gathers the given django.management.BaseCommand instance's default options
    and returns them as a dictionary.
    
    """
    return dict([
        get_option_default(option) for option in command.option_list])


def issubpackage(package, parents):
    if isinstance(parents, str):
        parents = (parents,)
    return len(parents) > 0 and reduce(
        bool.__or__,
        [parent == ".".join(package.split(".")[:len(parts)])
            for parent, parts in [(parent, parent.split("."))
                for parent in parents]],
        False)


def get_command_class_from_apps(name, apps, exclude_packages=None, exclude_command_class=None):
    """
    Searches through the given apps to find the named command class. Skips
    over any packages specified by exclude_packages and any command class
    specified by exclude_command_class. Returns the last command class found
    or None if the command class could not be found.
    
    Django's command searching behavior is backwards with respect to other
    features like template and static file loaders. This function follows
    that convention.
    
    """
    if exclude_packages is None:
        exclude_packages = []
    for app in reversed(
        [app for app in apps if not issubpackage(app, exclude_packages)]):
        try:
            command_class = import_module(
                "{app:s}.management.commands.{name:s}".format(
                    app=app, name=name)).Command
        except (ImportError, AttributeError):
            pass
        else:
            if exclude_command_class is None or \
                not issubclass(command_class, exclude_command_class):
                return command_class
    return None


def get_command_class(name, exclude_packages=None, exclude_command_class=None):
    """
    Searches "django.core" and the apps in settings.INSTALLED_APPS to find the
    named command class, optionally skipping packages or a particular
    command class.
    
    """
    from django.conf import settings
    return get_command_class_from_apps(
        name, 
        settings.INSTALLED_APPS \
            if "django.core" in settings.INSTALLED_APPS \
            else ("django.core",) + tuple(settings.INSTALLED_APPS),
        exclude_packages=exclude_packages,
        exclude_command_class=exclude_command_class)


def get_command_and_defaults(name, exclude_packages=None, exclude_command_class=None):
    """
    Searches "django.core" and the apps in settings.INSTALLED_APPS to find the
    named command class, optionally skipping packages or a particular command
    class. Gathers the command's default options and returns the command and
    options dictionary as a two-tuple: (command, options). Returns (None, {})
    if the command class could not be found.
    
    """
    command = get_command_class(name,
        exclude_packages=exclude_packages,
        exclude_command_class=exclude_command_class)
    defaults = {}
    if command is not None:
        command = command()
        defaults = command.get_option_defaults() \
            if isinstance(command, Command) \
            else get_option_defaults(command)
    return (command, defaults)


def check_command(self, name, exclude_packages=None, exclude_command_class=None):
    """
    Uses get_command_class() to check for the presence of a command.
    
    """
    return get_command_class(
        name, 
        exclude_packages=exclude_packages,
        exclude_command_class=exclude_command_class) is not None


def check_program(name):
    """
    Uses the shell program "which" to determine whether the named program
    is available on the shell PATH.
    
    """
    with open(os.devnull, "w") as null:
        try:
            subprocess.check_call(("which", name), stdout=null, stderr=null)
        except subprocess.CalledProcessError as e:
            return False
    return True


class devnull():
    """
    A context manager that returns the bit bucket opened for writing. Can be
    safely nested.
    
    """
    depth = 0
    null = None
    
    def __enter__(self):
        if self.depth == 0:
            self.null = open(os.devnull, "w")
        self.depth += 1
        return self.null
    
    def __exit__(self, *args, **kwargs):
        if self.depth == 1:
            self.null.close()
            self.null = None
        self.depth -= 1



class CommandOptions(object):
    """
    Command options mixin.
    
    """
    args = ""
    help = ""
    option_list = ()
    option_groups = ()
    actions = ()
    
    devnull = devnull()
    
    def get_option_list(self):
        """
        A hook to override the option list.
        
        """
        return self.option_list
    
    def get_option_groups(self):
        """
        A hook to override the option groups.
        
        """
        return self.option_groups
    
    def get_actions(self):
        """
        A hook to override the actions.
        
        """
        return self.actions
    
    def get_option_lists(self):
        """
        A hook to override the option lists used to generate option names
        and defaults.
        
        """
        return [self.get_option_list()] + \
            [option_list
                for name, description, option_list
                in self.get_option_groups()]
    
    def get_options(self):
        """
        A hook to override the flattened list of all options used to generate
        option names and defaults.
        
        """
        return reduce(
            list.__add__,
            [list(option_list) for option_list in self.get_option_lists()],
            [])
    
    def get_option_names(self):
        """
        A hook to override a list of all option names.
        
        """
        return [option.dest for option in self.get_options()]
    
    def get_option_defaults(self):
        """
        A hook to override a dictionary of all option defaults.
        
        """
        return dict([
            get_option_default(option) for option in self.get_options()])


class Command(CommandOptions, management.BaseCommand):
    """
    Command.
    
    """
    def usage(self, subcommand):
        """
        Customize the usage display.
        
        """
        usage = "%prog {subcommand:s} {args:}".format(
            subcommand=subcommand, args=self.args)
        if self.help:
            return "{usage:s}\n\n{help:s}".format(
                usage=usage, help=self.help)
        return usage
    
    def create_parser(self, prog_name, subcommand):
        """
        Customize the parser to include option groups.
        
        """
        parser = optparse.OptionParser(
            prog=prog_name,
            usage=self.usage(subcommand),
            version=self.get_version(),
            option_list=self.get_option_list())
        for name, description, option_list in self.get_option_groups():
            group = optparse.OptionGroup(parser, name, description);
            list(map(group.add_option, option_list))
            parser.add_option_group(group)
        return parser
    
    def parse_arguments(self, arguments):
        """
        Performs any required parsing on the argument values from optparse.
        
        """
        return arguments
    
    def parse_options(self, options):
        """
        Perform any required parsing on the option values from optparse.
        Attempts to call a parse_option_<name> method for each option name
        returned by self.get_option_names().
        
        """
        for name in self.get_option_names():
            parse = getattr(self, "parse_option_{name:s}".format(
                name=name), None)
            if parse is not None and isinstance(parse, collections.Callable):
                options[name] = parse()
        return options
    
    def handle(self, *arguments, **options):
        """
        Parses arguments and options, runs validate_<action> for each action
        named by self.get_actions(), then runs handle_<action> for each action
        named by self.get_actions().
        
        """
        self.arguments = arguments
        self.options = options
        self.arguments = self.parse_arguments(arguments)
        self.options = self.parse_options(options)
        
        for name in self.get_actions():
            validate = getattr(self, "validate_{name:s}".format(
                name=name), None)
            if validate is not None and isinstance(validate, collections.Callable):
                validate(*arguments, **options)
        for name in self.get_actions():
            handle = getattr(self, "handle_{name:s}".format(
                name=name), None)
            if handle is not None and isinstance(handle, collections.Callable):
                handle(*self.arguments, **self.options)


class BaseCommandOptions(CommandOptions):
    """
    Base Django management command options. Provides features to check for
    existence and call other management commands and shell programs.
    
    """
    exclude_packages = ("commando",)
    option_list = management.BaseCommand.option_list
    option_groups = (
        ("[standard options]",
            "Standard Django management command options.",
            option_list,
        ),
    )
    
    def get_exclude_packages(self):
        """
        A hook to override excluded packages when checking or running other
        management commands with check_command() or call_command.
        
        """
        return self.exclude_packages
    
    def parse_option_verbosity(self):
        try:
            verbosity = min(3, max(0, int(self.options.get("verbosity", 1))))
        except (ValueError, TypeError):
            verbosity = 1
        return verbosity
    
    def check_command(self, name):
        """
        Checks whether the given Django management command exists, excluding
        this command from the search.
        
        """
        if not check_command(
            name, 
            exclude_packages=self.get_exclude_packages(),
            exclude_command_class=self.__class__):
            raise management.CommandError(
                "The management command \"{name:s}\" is not available. "
                "Please ensure that you've added the application with "
                "the \"{name:s}\" command to your INSTALLED_APPS "
                "setting".format(
                    name=name))
    
    def check_program(self, name):
        """
        Checks whether a program is available on the shell PATH.
        
        """
        if not check_program(name):
            raise management.CommandError(
                "The program \"{name:s}\" is not available in the shell. "
                "Please ensure that \"{name:s}\" is installed and reachable "
                "through your PATH environment variable.".format(
                    name=name))
    
    def call_command(self, name, *arguments, **options):
        """
        Finds the given Django management command and default options,
        excluding this command, and calls it with the given arguments
        and override options.
        
        """
        command, defaults = get_command_and_defaults(
            name,
            exclude_packages=self.get_exclude_packages(),
            exclude_command_class=self.__class__)
        if command is None:
            raise management.CommandError(
                "Unknown command: {name:s}".format(
                    name=name))
        defaults.update(options)
        return command.execute(*arguments, **defaults)
    
    def call_program(self, name, *arguments):
        """
        Calls the shell program on the PATH with the given arguments.
        
        """
        verbosity = self.options.get("verbosity", 1)
        with self.devnull as null:
            try:
                subprocess.check_call((name,) + tuple(arguments), 
                    stdout=null if verbosity == 0 else self.stdout,
                    stderr=null if verbosity == 0 else self.stderr)
            except subprocess.CalledProcessError as error:
                raise management.CommandError(
                    "{name:s} failed with exit code {code:d}".format(
                        name=name, code=error.returncode))
        return 0


class BaseCommand(BaseCommandOptions, Command):
    """
    Base Django management command.
    
    """
    option_list = ()
