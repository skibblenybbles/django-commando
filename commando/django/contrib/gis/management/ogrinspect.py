from commando import management


BaseOGRInspectCommand = management.get_command_class(
    "ogrinspect", exclude_packages=("commando",))

if BaseOGRInspectCommand is not None:
    
    base = BaseOGRInspectCommand()
    
    class OGRInspectCommandOptions(management.CommandOptions):
        """
        OGRInspect command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[ogrinspect options]",
                "These options will be passed to ogrinspect.",
                option_list,
            ),) if option_list else ()
        actions = ("ogrinspect",)
        
        def handle_ogrinspect(self, *args, **options):
            return self.call_command("ogrinspect", *args, **options)
    
    
    class OGRInspectCommand(OGRInspectCommandOptions, management.StandardCommand):
        """
        OGRInspect command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            OGRInspectCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    OGRInspectCommand = management.StandardCommand
