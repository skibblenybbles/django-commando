from commando import management


BaseBuildSolrSchemaCommand = management.get_command_class(
    "build_solr_schema", exclude_packages=("commando",))

if BaseBuildSolrSchemaCommand is not None:
    
    base = BaseBuildSolrSchemaCommand()
    
    class BuildSolrSchemaCommandOptions(management.CommandOptions):
        """
        BuildSolrSchema command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[build_solr_schema options]",
                "These options will be passed to build_solr_schema.",
                option_list,
            ),) if option_list else ()
        actions = ("build_solr_schema",)
        
        def handle_build_solr_schema(self, *args, **options):
            return self.call_command("build_solr_schema", *args, **options)
    
    
    class BuildSolrSchemaCommand(BuildSolrSchemaCommandOptions, management.StandardCommand):
        """
        BuildSolrSchema command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            BuildSolrSchemaCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    BuildSolrSchemaCommand = management.StandardCommand
