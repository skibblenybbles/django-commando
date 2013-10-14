from commando import management


BaseSchemaMigrationCommand = management.get_command_class(
    "schemamigration", exclude_packages=("commando",))

if BaseSchemaMigrationCommand is not None:
    
    base = BaseSchemaMigrationCommand()
    
    class SchemaMigrationCommandOptions(management.CommandOptions):
        """
        SchemaMigration command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[schemamigration options]",
                "These options will be passed to schemamigration.",
                option_list,
            ),) if option_list else ()
        actions = ("schemamigration",)
        
        def handle_schemamigration(self, *args, **options):
            return self.call_command("schemamigration", *args, **options)
    
    
    class SchemaMigrationCommand(SchemaMigrationCommandOptions, management.StandardCommand):
        """
        SchemaMigration command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SchemaMigrationCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SchemaMigrationCommand = management.StandardCommand
