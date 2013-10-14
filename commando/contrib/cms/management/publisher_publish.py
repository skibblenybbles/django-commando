from commando import management


BasePublisherPublishCommand = management.get_command_class(
    "publisher_publish", exclude_packages=("commando",))

if BasePublisherPublishCommand is not None:
    
    base = BasePublisherPublishCommand()
    
    class PublisherPublishCommandOptions(management.CommandOptions):
        """
        PublisherPublish command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[publisher_publish options]",
                "These options will be passed to publisher_publish.",
                option_list,
            ),) if option_list else ()
        actions = ("publisher_publish",)
        
        def handle_publisher_publish(self, *args, **options):
            return self.call_command("publisher_publish", *args, **options)
    
    
    class PublisherPublishCommand(PublisherPublishCommandOptions, management.StandardCommand):
        """
        PublisherPublish command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            PublisherPublishCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    PublisherPublishCommand = management.StandardCommand
