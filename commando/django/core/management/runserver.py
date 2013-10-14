from commando import management


BaseRunServerCommand = management.get_command_class(
    "runserver", exclude_packages=("commando",))

if BaseRunServerCommand is not None:
    
    base = BaseRunServerCommand()
    
    class RunServerCommandOptions(management.CommandOptions):
        """
        RunServer command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[runserver options]",
                "These options will be passed to runserver.",
                option_list,
            ),) if option_list else ()
        actions = ("runserver",)
        
        def handle_runserver(self, *args, **options):
            return self.call_command("runserver", *args, **options)
    
    
    class RunServerCommand(RunServerCommandOptions, management.StandardCommand):
        """
        RunServer command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            RunServerCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    RunServerCommand = management.StandardCommand
