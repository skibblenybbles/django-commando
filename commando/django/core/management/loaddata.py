from commando import management


BaseLoadDataCommand = management.get_command_class(
    "loaddata", exclude_packages=("commando",))

if BaseLoadDataCommand is not None:
    
    base = BaseLoadDataCommand()
    
    class LoadDataCommandOptions(management.CommandOptions):
        """
        LoadData command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[loaddata options]",
                "These options will be passed to loaddata.",
                option_list,
            ),) if option_list else ()
        actions = ("loaddata",)
        
        def handle_loaddata(self, *args, **options):
            return self.call_command("loaddata", *args, **options)
    
    
    class LoadDataCommand(LoadDataCommandOptions, management.StandardCommand):
        """
        LoadData command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            LoadDataCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    LoadDataCommand = management.StandardCommand
