from commando import management


BaseClearIndexCommand = management.get_command_class(
    "clear_index", exclude_packages=("commando",))

if BaseClearIndexCommand is not None:
    
    base = BaseClearIndexCommand()
    
    class ClearIndexCommandOptions(management.CommandOptions):
        """
        ClearIndex command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[clear_index options]",
                "These options will be passed to clear_index.",
                option_list,
            ),) if option_list else ()
        actions = ("clear_index",)
        
        def handle_clear_index(self, *args, **options):
            return self.call_command("clear_index", *args, **options)
    
    
    class ClearIndexCommand(ClearIndexCommandOptions, management.StandardCommand):
        """
        ClearIndex command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            ClearIndexCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    ClearIndexCommand = management.StandardCommand
