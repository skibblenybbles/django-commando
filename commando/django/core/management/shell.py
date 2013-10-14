from commando import management


BaseShellCommand = management.get_command_class(
    "shell", exclude_packages=("commando",))

if BaseShellCommand is not None:
    
    base = BaseShellCommand()
    
    class ShellCommandOptions(management.CommandOptions):
        """
        Shell command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[shell options]",
                "These options will be passed to shell.",
                option_list,
            ),) if option_list else ()
        actions = ("shell",)
        
        def handle_shell(self, *args, **options):
            return self.call_command("shell", *args, **options)
    
    
    class ShellCommand(ShellCommandOptions, management.StandardCommand):
        """
        Shell command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            ShellCommandOptions.option_groups + \
            management.StandardCommand.option_groups
        
else:
    
    ShellCommand = management.StandardCommand
