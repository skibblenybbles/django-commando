from commando import management


BaseDataMigrationCommand = management.get_command_class(
    "datamigration", exclude_packages=("commando",))

if BaseDataMigrationCommand is not None:
    
    base = BaseDataMigrationCommand()
    
    class DataMigrationCommandOptions(management.CommandOptions):
        """
        DataMigration command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[datamigration options]",
                "These options will be passed to datamigration.",
                option_list,
            ),) if option_list else ()
        actions = ("datamigration",)
        
        def handle_datamigration(self, *args, **options):
            return self.call_command("datamigration", *args, **options)
    
    
    class DataMigrationCommand(DataMigrationCommandOptions, management.StandardCommand):
        """
        DataMigration command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            DataMigrationCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    DataMigrationCommand = management.StandardCommand
