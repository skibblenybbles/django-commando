from commando import management


BaseStartAppCommand = management.get_command_class(
    "startapp", exclude_packages=("commando",))

if BaseStartAppCommand is not None:
    
    base = BaseStartAppCommand()
    
    class StartAppCommandOptions(management.CommandOptions):
        """
        StartApp command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[startapp options]",
                "These options will be passed to startapp.",
                option_list,
            ),) if option_list else ()
        actions = ("startapp",)
        
        def handle_startapp(self, *args, **options):
            return self.call_command("startapp", *args, **options)
    
    
    class StartAppCommand(StartAppCommandOptions, management.StandardCommand):
        """
        StartApp command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            StartAppCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    StartAppCommand = management.StandardCommand
