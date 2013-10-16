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
