from django.core.management import CommandError

from commando import management


class GrepCommandOptions(management.CommandOptions):
    args = "[pattern]"
    help = "Search current directory for a regular expression pattern"
    option_list = ()
    option_groups = ()
    actions = ("grep",)
    
    def validate_grep(self, *arguments, **options):
        # Make sure this command was called with one argument.
        if not len(arguments) == 1:
            raise CommandError(
                "You must provide a single regular expression pattern")
        
        # Make sure grep is available in the shell.
        self.check_program("grep")
    
    def handle_grep(self, pattern, **options):
        self.call_program("grep", "-nrI", "-P", pattern, ".")


class GrepCommand(GrepCommandOptions, management.StandardCommand):
    option_list = management.StandardCommand.option_list
    option_groups = \
        GrepCommandOptions.option_groups + \
        management.StandardCommand.option_groups
