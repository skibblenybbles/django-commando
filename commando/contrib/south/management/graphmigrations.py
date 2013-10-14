from commando import management


BaseGraphMigrationsCommand = management.get_command_class(
    "graphmigrations", exclude_packages=("commando",))

if BaseGraphMigrationsCommand is not None:
    
    class GraphMigrationsCommandOptions(management.CommandOptions):
        """
        GraphMigrations command options.
        
        """
        args = BaseGraphMigrationsCommand.args
        help = BaseGraphMigrationsCommand.help
        option_list = BaseGraphMigrationsCommand.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[graphmigrations options]",
                "These options will be passed to graphmigrations.",
                option_list,
            ),) if option_list else ()
        actions = ("graphmigrations",)
        
        def handle_graphmigrations(self, *args, **options):
            return self.call_command("graphmigrations", *args, **options)
    
    
    class GraphMigrationsCommand(GraphMigrationsCommandOptions, management.StandardCommand):
        """
        GraphMigrations command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            GraphMigrationsCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    GraphMigrationsCommand = management.StandardCommand
