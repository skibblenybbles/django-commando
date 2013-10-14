from commando import management


BaseStartProjectCommand = management.get_command_class(
    "startproject", exclude_packages=("commando",))

if BaseStartProjectCommand is not None:
    
    base = BaseStartProjectCommand()
    
    class StartProjectCommandOptions(management.CommandOptions):
        """
        StartProject command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[startproject options]",
                "These options will be passed to startproject.",
                option_list,
            ),) if option_list else ()
        actions = ("startproject",)
        
        def handle_startproject(self, *args, **options):
            return self.call_command("startproject", *args, **options)
    
    
    class StartProjectCommand(StartProjectCommandOptions, management.StandardCommand):
        """
        StartProject command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            StartProjectCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    StartProjectCommand = management.StandardCommand
