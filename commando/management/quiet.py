import optparse

from . import base


class QuietCommandOptions(base.CommandOptions):
    """
    Quiet Django management command options.
    
    """
    option_list = (
        optparse.make_option("-q", "--quiet",
            action="store_true", dest="quiet", default=False,
            help="Suppress all prompts and output."),)
    quiet_option_names = (
        ("interactive", False),
        ("verbosity", 0),)
    
    def get_quiet_option_names(self):
        """
        A hook to override the two-tuples for option values that
        should be set when the quiet option is True.
        
        """
        return self.quiet_option_names
    
    def parse_option_quiet(self):
        quiet = bool(self.options.get("quiet", False))
        if quiet:
            for name, value in self.get_quiet_option_names():
                self.options[name] = value
        return quiet


class QuietCommand(QuietCommandOptions, base.Command):
    """
    Quiet Django management command.
    
    """
    pass
