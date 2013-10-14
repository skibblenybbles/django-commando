from commando import management


BaseMigrationCheckCommand = management.get_command_class(
    "migrationcheck", exclude_packages=("commando",))

if BaseMigrationCheckCommand is not None:
    
    base = BaseMigrationCheckCommand()
    
    class MigrationCheckCommandOptions(management.CommandOptions):
        """
        MigrationCheck command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[migrationcheck options]",
                "These options will be passed to migrationcheck.",
                option_list,
            ),) if option_list else ()
        actions = ("migrationcheck",)
        
        def handle_migrationcheck(self, *args, **options):
            return self.call_command("migrationcheck", *args, **options)
    
    
    class MigrationCheckCommand(MigrationCheckCommandOptions, management.StandardCommand):
        """
        MigrationCheck command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            MigrationCheckCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    MigrationCheckCommand = management.StandardCommand
