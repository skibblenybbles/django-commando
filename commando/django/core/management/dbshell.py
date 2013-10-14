from commando import management


BaseDBShellCommand = management.get_command_class(
    "dbshell", exclude_packages=("commando",))

if BaseDBShellCommand is not None:
    
    base = BaseDBShellCommand()
    
    class DBShellCommandOptions(management.CommandOptions):
        """
        Database shell command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[dbshell options]",
                "These options will be passed to dbshell.",
                option_list,
            ),) if option_list else ()
        actions = ("dbshell",)
        
        def handle_dbshell(self, *args, **options):
            return self.call_command("dbshell", *args, **options)
    
    
    class DBShellCommand(DBShellCommandOptions, management.StandardCommand):
        """
        Database shell command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            DBShellCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    DBShellCommand = management.StandardCommand
