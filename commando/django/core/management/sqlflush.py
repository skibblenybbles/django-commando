from commando import management


BaseSQLFlushCommand = management.get_command_class(
    "sqlflush", exclude_packages=("commando",))

if BaseSQLFlushCommand is not None:
    
    class SQLFlushCommandOptions(management.CommandOptions):
        """
        SQLFlush command options.
        
        """
        args = BaseSQLFlushCommand.args
        help = BaseSQLFlushCommand.help
        option_list = BaseSQLFlushCommand.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[sqlflush options]",
                "These options will be passed to sqlflush.",
                option_list,
            ),) if option_list else ()
        actions = ("sqlflush",)
        
        def handle_sqlflush(self, *args, **options):
            return self.call_command("sqlflush", *args, **options)
    
    
    class SQLFlushCommand(SQLFlushCommandOptions, management.StandardCommand):
        """
        SQLFlush command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SQLFlushCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SQLFlushCommand = management.StandardCommand
