from commando import management


BaseCMSCommand = management.get_command_class(
    "cms", exclude_packages=("commando",))

if BaseCMSCommand is not None:
    
    base = BaseCMSCommand()
    
    class CMSCommandOptions(management.CommandOptions):
        """
        CMS command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[cms options]",
                "These options will be passed to cms.",
                option_list,
            ),) if option_list else ()
        actions = ("cms",)
        subcommands = base.subcommands
        
        def handle_cms(self, *args, **options):
            return self.call_command("cms", *args, **options)
    
    
    class CMSCommand(CMSCommandOptions, management.StandardCommand):
        """
        CMS command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            CMSCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    CMSCommand = management.StandardCommand
