from commando import management


BaseCreateSuperuserCommand = management.get_command_class(
    "createsuperuser", exclude_packages=("commando",))

if BaseCreateSuperuserCommand is not None:
    
    base = BaseCreateSuperuserCommand()
    
    class CreateSuperuserCommandOptions(management.CommandOptions):
        """
        CreateSuperuser command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[createsuperuser options]",
                "These options will be passed to createsuperuser.",
                option_list,
            ),) if option_list else ()
        actions = ("createsuperuser",)
        
        def handle_createsuperuser(self, *args, **options):
            return self.call_command("createsuperuser", *args, **options)
    
    
    class CreateSuperuserCommand(CreateSuperuserCommandOptions, management.StandardCommand):
        """
        CreateSuperuser command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            CreateSuperuserCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    CreateSuperuserCommand = management.StandardCommand
