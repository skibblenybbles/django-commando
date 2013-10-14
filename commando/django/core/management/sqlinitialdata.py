from commando import management


BaseSQLInitialDataCommand = management.get_command_class(
    "sqlinitialdata", exclude_packages=("commando",))

if BaseSQLInitialDataCommand is not None:
    
    class SQLInitialDataCommandOptions(management.CommandOptions):
        """
        SQLInitialData command options.
        
        """
        args = BaseSQLInitialDataCommand.args
        help = BaseSQLInitialDataCommand.help
        option_list = BaseSQLInitialDataCommand.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[sqlinitialdata options]",
                "These options will be passed to sqlinitialdata.",
                option_list,
            ),) if option_list else ()
        actions = ("sqlinitialdata",)
        
        def handle_sqlinitialdata(self, *args, **options):
            return self.call_command("sqlinitialdata", *args, **options)
    
    
    class SQLInitialDataCommand(SQLInitialDataCommandOptions, management.StandardCommand):
        """
        SQLInitialData command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SQLInitialDataCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SQLInitialDataCommand = management.StandardCommand
