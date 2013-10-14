from commando import management


BaseInspectDBCommand = management.get_command_class(
    "inspectdb", exclude_packages=("commando",))

if BaseInspectDBCommand is not None:
    
    base = BaseInspectDBCommand()
    
    class InspectDBCommandOptions(management.CommandOptions):
        """
        InspectDB command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[inspectdb options]",
                "These options will be passed to inspectdb.",
                option_list,
            ),) if option_list else ()
        actions = ("inspectdb",)
        
        def handle_inspectdb(self, *args, **options):
            return self.call_command("inspectdb", *args, **options)
    
    
    class InspectDBCommand(InspectDBCommandOptions, management.StandardCommand):
        """
        InspectDB command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            InspectDBCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    InspectDBCommand = management.StandardCommand
