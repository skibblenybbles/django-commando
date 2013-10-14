from commando import management


BaseSQLClearCommand = management.get_command_class(
    "sqlclear", exclude_packages=("commando",))

if BaseSQLClearCommand is not None:
    
    class SQLClearCommandOptions(management.CommandOptions):
        """
        SQLClear command options.
        
        """
        args = BaseSQLClearCommand.args
        help = BaseSQLClearCommand.help
        option_list = BaseSQLClearCommand.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[sqlclear options]",
                "These options will be passed to sqlclear.",
                option_list,
            ),) if option_list else ()
        actions = ("sqlclear",)
        
        def handle_sqlclear(self, *args, **options):
            return self.call_command("sqlclear", *args, **options)
    
    
    class SQLClearCommand(SQLClearCommandOptions, management.StandardCommand):
        """
        SQLClear command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SQLClearCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SQLClearCommand = management.StandardCommand
