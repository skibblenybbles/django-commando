from commando import management


BaseMigrateCommand = management.get_command_class(
    "migrate", exclude_packages=("commando",))

if BaseMigrateCommand is not None:
    
    base = BaseMigrateCommand()
    
    class MigrateCommandOptions(management.CommandOptions):
        """
        Migrate command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[migrate options]",
                "These options will be passed to migrate.",
                option_list,
            ),) if option_list else ()
        actions = ("migrate",)
        
        def handle_migrate(self, *args, **options):
            return self.call_command("migrate", *args, **options)
    
    
    class MigrateCommand(MigrateCommandOptions, management.StandardCommand):
        """
        Migrate command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            MigrateCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    MigrateCommand = management.StandardCommand
