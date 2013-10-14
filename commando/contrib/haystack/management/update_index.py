from commando import management


BaseUpdateIndexCommand = management.get_command_class(
    "update_index", exclude_packages=("commando",))

if BaseUpdateIndexCommand is not None:
    
    base = BaseUpdateIndexCommand()
    
    class UpdateIndexCommandOptions(management.CommandOptions):
        """
        UpdateIndex command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[update_index options]",
                "These options will be passed to update_index.",
                option_list,
            ),) if option_list else ()
        actions = ("update_index",)
        
        def handle_update_index(self, *args, **options):
            return self.call_command("update_index", *args, **options)
    
    
    class UpdateIndexCommand(UpdateIndexCommandOptions, management.StandardCommand):
        """
        UpdateIndex command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            UpdateIndexCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    UpdateIndexCommand = management.StandardCommand
