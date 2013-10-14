from commando import management


BaseSQLCommand = management.get_command_class(
    "sql", exclude_packages=("commando",))

if BaseSQLCommand is not None:
    
    base = BaseSQLCommand()
    
    class SQLCommandOptions(management.CommandOptions):
        """
        SQL command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[sql options]",
                "These options will be passed to sql.",
                option_list,
            ),) if option_list else ()
        actions = ("sql",)
        
        def handle_sql(self, *args, **options):
            return self.call_command("sql", *args, **options)
    
    
    class SQLCommand(SQLCommandOptions, management.StandardCommand):
        """
        SQL command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SQLCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SQLCommand = management.StandardCommand
