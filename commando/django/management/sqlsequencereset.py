from commando import management


BaseSQLSequenceResetCommand = management.get_command_class(
    "sqlsequencereset", exclude_packages=("commando",))

if BaseSQLSequenceResetCommand is not None:
    
    class SQLSequenceResetCommandOptions(management.CommandOptions):
        """
        SQLSequenceReset command options.
        
        """
        args = BaseSQLSequenceResetCommand.args
        help = BaseSQLSequenceResetCommand.help
        option_list = BaseSQLSequenceResetCommand.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[sqlsequencereset options]",
                "These options will be passed to sqlsequencereset.",
                option_list,
            ),) if option_list else ()
        actions = ("sqlsequencereset",)
        
        def handle_sqlsequencereset(self, *args, **options):
            return self.call_command("sqlsequencereset", *args, **options)
    
    
    class SQLSequenceResetCommand(SQLSequenceResetCommandOptions, management.StandardCommand):
        """
        SQLSequenceReset command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SQLSequenceResetCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SQLSequenceResetCommand = management.StandardCommand
