from commando import management


BaseSQLAllCommand = management.get_command_class(
    "sqlall", exclude_packages=("commando",))

if BaseSQLAllCommand is not None:
    
    base = BaseSQLAllCommand()
    
    class SQLAllCommandOptions(management.CommandOptions):
        """
        SQLAll command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[sqlall options]",
                "These options will be passed to sqlall.",
                option_list,
            ),) if option_list else ()
        actions = ("sqlall",)
        
        def handle_sqlall(self, *args, **options):
            return self.call_command("sqlall", *args, **options)
    
    
    class SQLAllCommand(SQLAllCommandOptions, management.StandardCommand):
        """
        SQLAll command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SQLAllCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SQLAllCommand = management.StandardCommand
