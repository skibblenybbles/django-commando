from commando import management


BaseConvertToSouthCommand = management.get_command_class(
    "convert_to_south", exclude_packages=("commando",))

if BaseConvertToSouthCommand is not None:
    
    base = BaseConvertToSouthCommand()
    
    class ConvertToSouthCommandOptions(management.CommandOptions):
        """
        ConvertToSouth command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[convert_to_south options]",
                "These options will be passed to convert_to_south.",
                option_list,
            ),) if option_list else ()
        actions = ("convert_to_south",)
        
        def handle_convert_to_south(self, *args, **options):
            return self.call_command("convert_to_south", *args, **options)
    
    
    class ConvertToSouthCommand(ConvertToSouthCommandOptions, management.StandardCommand):
        """
        ConvertToSouth command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            ConvertToSouthCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    ConvertToSouthCommand = management.StandardCommand
