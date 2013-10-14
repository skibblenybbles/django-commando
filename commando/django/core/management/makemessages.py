from commando import management


BaseMakeMessagesCommand = management.get_command_class(
    "makemessages", exclude_packages=("commando",))

if BaseMakeMessagesCommand is not None:
    
    base = BaseMakeMessagesCommand()
    
    class MakeMessagesCommandOptions(management.CommandOptions):
        """
        MakeMessages command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[makemessages options]",
                "These options will be passed to makemessages.",
                option_list,
            ),) if option_list else ()
        actions = ("makemessages",)
        
        def handle_makemessages(self, *args, **options):
            return self.call_command("makemessages", *args, **options)
    
    
    class MakeMessagesCommand(MakeMessagesCommandOptions, management.StandardCommand):
        """
        MakeMessages command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            MakeMessagesCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    MakeMessagesCommand = management.StandardCommand
