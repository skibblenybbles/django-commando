from commando import management


BaseDiffSettingsCommand = management.get_command_class(
    "diffsettings", exclude_packages=("commando",))

if BaseDiffSettingsCommand is not None:
    
    base = BaseDiffSettingsCommand()
    
    class DiffSettingsCommandOptions(management.CommandOptions):
        """
        Diff settings command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[diffsettings options]",
                "These options will be passed to diffsettings.",
                option_list,
            ),) if option_list else ()
        actions = ("diffsettings",)
        
        def handle_diffsettings(self, *args, **options):
            return self.call_command("diffsettings", *args, **options)
    
    
    class DiffSettingsCommand(DiffSettingsCommandOptions, management.StandardCommand):
        """
        Diff settings command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            DiffSettingsCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    DiffSettingsCommand = management.StandardCommand
