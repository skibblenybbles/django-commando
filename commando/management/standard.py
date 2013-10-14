from django.core import management

from . import base
from . import quiet


class StandardCommandOptions(base.CommandOptions):
    """
    Standard command options mixin.
    
    """
    help = "Unimplemented command."
    option_list = quiet.QuietCommandOptions.option_list
    option_groups = base.BaseCommandOptions.option_groups
    actions = ("error",)
    
    def handle_error(self, *args, **kwargs):
        raise management.CommandError("This command is not implemented")
    

class StandardCommand(StandardCommandOptions, quiet.QuietCommand, base.BaseCommand):
    """
    Base class for enhanced, standard Django commands.
    
    """
    pass
