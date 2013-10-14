from commando import management


BaseRunFCGICommand = management.get_command_class(
    "runfcgi", exclude_packages=("commando",))

if BaseRunFCGICommand is not None:
    
    base = BaseRunFCGICommand()
    
    class RunFCGICommandOptions(management.CommandOptions):
        """
        RunFCGI command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[runfcgi options]",
                "These options will be passed to runfcgi.",
                option_list,
            ),) if option_list else ()
        actions = ("runfcgi",)
        
        def handle_runfcgi(self, *args, **options):
            return self.call_command("runfcgi", *args, **options)
    
    
    class RunFCGICommand(RunFCGICommandOptions, management.StandardCommand):
        """
        RunFCGI command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            RunFCGICommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    RunFCGICommand = management.StandardCommand
