from commando import management


BaseFlushCommand = management.get_command_class(
    "flush", exclude_packages=("commando",))

if BaseFlushCommand is not None:
    
    class FlushCommandOptions(management.CommandOptions):
        """
        Flush command options.
        
        """
        args = BaseFlushCommand.args
        help = BaseFlushCommand.help
        option_list = BaseFlushCommand.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[flush options]",
                "These options will be passed to flush.",
                option_list,
            ),) if option_list else ()
        actions = ("flush",)
        
        def handle_flush(self, *args, **options):
            return self.call_command("flush", *args, **options)
    
    
    class FlushCommand(FlushCommandOptions, management.StandardCommand):
        """
        Flush command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            FlushCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    FlushCommand = management.StandardCommand
