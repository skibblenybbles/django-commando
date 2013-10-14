from commando import management


BaseSQLCustomCommand = management.get_command_class(
    "sqlcustom", exclude_packages=("commando",))

if BaseSQLCustomCommand is not None:
    
    base = BaseSQLCustomCommand()
    
    class SQLCustomCommandOptions(management.CommandOptions):
        """
        SQLCustom command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[sqlcustom options]",
                "These options will be passed to sqlcustom.",
                option_list,
            ),) if option_list else ()
        actions = ("sqlcustom",)
        
        def handle_sqlcustom(self, *args, **options):
            return self.call_command("sqlcustom", *args, **options)
    
    
    class SQLCustomCommand(SQLCustomCommandOptions, management.StandardCommand):
        """
        SQLCustom command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SQLCustomCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SQLCustomCommand = management.StandardCommand
