from commando import management


BaseSQLIndexesCommand = management.get_command_class(
    "sqlindexes", exclude_packages=("commando",))

if BaseSQLIndexesCommand is not None:
    
    base = BaseSQLIndexesCommand()
    
    class SQLIndexesCommandOptions(management.CommandOptions):
        """
        SQLIndexes command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[sqlindexes options]",
                "These options will be passed to sqlindexes.",
                option_list,
            ),) if option_list else ()
        actions = ("sqlindexes",)
        
        def handle_sqlindexes(self, *args, **options):
            return self.call_command("sqlindexes", *args, **options)
    
    
    class SQLIndexesCommand(SQLIndexesCommandOptions, management.StandardCommand):
        """
        SQLIndexes command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SQLIndexesCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SQLIndexesCommand = management.StandardCommand
