from commando import management


BaseClearSessionsCommand = management.get_command_class(
    "clearsessions", exclude_packages=("commando",))

if BaseClearSessionsCommand is not None:
    
    base = BaseClearSessionsCommand()
    
    class ClearSessionsCommandOptions(management.CommandOptions):
        """
        ClearSessions command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[clearsessions options]",
                "These options will be passed to clearsessions.",
                option_list,
            ),) if option_list else ()
        actions = ("clearsessions",)
        
        def handle_clearsessions(self, *args, **options):
            return self.call_command("clearsessions", *args, **options)
    
    
    class ClearSessionsCommand(ClearSessionsCommandOptions, management.StandardCommand):
        """
        ClearSessions command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            ClearSessionsCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    ClearSessionsCommand = management.StandardCommand
