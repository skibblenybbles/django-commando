from commando import management


BaseValidateCommand = management.get_command_class(
    "validate", exclude_packages=("commando",))

if BaseValidateCommand is not None:
    
    base = BaseValidateCommand()
    
    class ValidateCommandOptions(management.CommandOptions):
        """
        Validate command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[validate options]",
                "These options will be passed to validate.",
                option_list,
            ),) if option_list else ()
        actions = ("validate",)
        
        def handle_validate(self, *args, **options):
            return self.call_command("validate", *args, **options)
    
    
    class ValidateCommand(ValidateCommandOptions, management.StandardCommand):
        """
        Validate command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            ValidateCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    ValidateCommand = management.StandardCommand
