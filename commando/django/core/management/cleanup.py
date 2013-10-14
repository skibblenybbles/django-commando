from commando import management


BaseCleanupCommand = management.get_command_class(
    "cleanup", exclude_packages=("commando",))

if BaseCleanupCommand is not None:
    
    base = BaseCleanupCommand()
    
    class CleanupCommandOptions(management.CommandOptions):
        """
        Cleanup command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[cleanup options]",
                "These options will be passed to cleanup.",
                option_list,
            ),) if option_list else ()
        actions = ("cleanup",)
        
        def handle_cleanup(self, *args, **options):
            return self.call_command("cleanup", *args, **options)
    
    
    class CleanupCommand(CleanupCommandOptions, management.StandardCommand):
        """
        Cleanup command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            CleanupCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    CleanupCommand = management.StandardCommand
