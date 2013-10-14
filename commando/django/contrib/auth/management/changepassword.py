from commando import management


BaseChangePasswordCommand = management.get_command_class(
    "changepassword", exclude_packages=("commando",))

if BaseChangePasswordCommand is not None:
    
    base = BaseChangePasswordCommand()
    
    class ChangePasswordCommandOptions(management.CommandOptions):
        """
        ChangePassword command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[changepassword options]",
                "These options will be passed to changepassword.",
                option_list,
            ),) if option_list else ()
        actions = ("changepassword",)
        
        def handle_changepassword(self, *args, **options):
            return self.call_command("changepassword", *args, **options)
    
    
    class ChangePasswordCommand(ChangePasswordCommandOptions, management.StandardCommand):
        """
        ChangePassword command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            ChangePasswordCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    ChangePasswordCommand = management.StandardCommand
