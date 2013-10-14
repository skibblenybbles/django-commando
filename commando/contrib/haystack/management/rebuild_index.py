from commando import management


BaseRebuildIndexCommand = management.get_command_class(
    "rebuild_index", exclude_packages=("commando",))

if BaseRebuildIndexCommand is not None:
    
    base = BaseRebuildIndexCommand()
    
    class RebuildIndexCommandOptions(management.CommandOptions):
        """
        RebuildIndex command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[rebuild_index options]",
                "These options will be passed to rebuild_index.",
                option_list,
            ),) if option_list else ()
        actions = ("rebuild_index",)
        
        def handle_rebuild_index(self, *args, **options):
            return self.call_command("rebuild_index", *args, **options)
    
    
    class RebuildIndexCommand(RebuildIndexCommandOptions, management.StandardCommand):
        """
        RebuildIndex command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            RebuildIndexCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    RebuildIndexCommand = management.StandardCommand
