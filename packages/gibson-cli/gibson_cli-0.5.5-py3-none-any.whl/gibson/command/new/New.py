import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.new.Module import Module
from gibson.command.new.Project import Project


class New(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()
        elif sys.argv[2] == "project":
            Project(self.configuration).execute()
        elif sys.argv[2] == "module":
            Module(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('new')} {Colors.arguments(['project', 'module'])} {Colors.hint('create something new')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('new')} {Colors.argument('project')} {Colors.hint('create a new project')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('new')} {Colors.argument('module')} {Colors.hint('create a new module')}\n"
        )
        self.conversation.newline()
        exit(1)
