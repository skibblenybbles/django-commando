from commando import management


BaseStartMigrationCommand = management.get_command_class(
    "startmigration", exclude_packages=("commando",))

if BaseStartMigrationCommand is not None:
    
    base = BaseStartMigrationCommand()
    
    class StartMigrationCommandOptions(management.CommandOptions):
        """
        StartMigration command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[startmigration options]",
                "These options will be passed to startmigration.",
                option_list,
            ),) if option_list else ()
        actions = ("startmigration",)
        
        def handle_startmigration(self, *args, **options):
            return self.call_command("startmigration", *args, **options)
    
    
    class StartMigrationCommand(StartMigrationCommandOptions, management.StandardCommand):
        """
        StartMigration command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            StartMigrationCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    StartMigrationCommand = management.StandardCommand
