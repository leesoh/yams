"""
Management shell for YAMS.

Current:
    * Search modules for string
    * Show module details
    * Create new module skeleton

Planned:
    * Create playbooks
    * Deploy playbooks
"""

import cmd
import json
import os
import readline
import textwrap
from pathlib import Path
from datetime import date

import texttable

# TODO: Evaluate moving these to NewModule
yams_dir = Path.cwd().parent
module_dir = Path(yams_dir, 'roles')

# Name of role-level documents
role_docs_name = 'docs.json'

# Allows nested cmd to exit parent
exit = False


def clear_screen():
    """Clear the screen on each OS."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Main(cmd.Cmd, object):
    """Main loop for YMS.

    Processes user input for top-level commands before passing the work
    off to other classes.

    Todo:
        * newmodule [modulename]

    Reference:
        * https://wiki.python.org/moin/CmdModule
        * https://github.com/EmpireProject/Empire/blob/73358262acc8ed3c34ffc87fa593655295b81434/lib/common/empire.py
    """

    intro = r"""

 __   ____  ___ _____
 \ \ / /  \/  |/  ___|
  \ V /| .  . |\ `--.
   \ / | |\/| | `--. \
   | | | |  | |/\__/ /
   \_/ \_|  |_/\____/

 The YAMS Management System v0.1
    """
    prompt = '[YMS] > '
    doc_header = 'Commands'
    ruler = '-'

    def __init__(self):
        """Init method for Main."""
        cmd.Cmd.__init__(self)  # Initialize parent
        self.searchmodule = SearchModule()  # Create SearchModule object
        self.newmodule = NewModule()  # Create NewModule object
        clear_screen()  # Clear screen before intro

    def show_main(self):
        """Show main menu splash screen."""
        clear_screen()
        print(self.intro)

    def do_newmodule(self, line):
        """Handle the 'newmodule' command.

        Args:
            line (str): user-submitted input, may have been auto-completed.

        """
        self.newmodule.prompt = self.prompt[:-4] + '::New Module] > '
        # TODO: How can we make cmdloop start with settings here?
        self.newmodule.cmdloop()
        return exit

    def help_newmodule(self):
        """Help for newmodule command."""
        print('\nUsage: newmodule\n')

    def do_searchmodule(self, line):
        """Handle the 'searchmodule' command.

        Calls the appropriate method of searchmodule.

        Args:
            line (str): user-submitted input, may have been auto-completed
        """
        self.searchmodule.search(line)

    def help_searchmodule(self):
        """Help for searchmodule command."""
        print('\nUsage: searchmodule [search term]\n')

    def do_showmodule(self, line):
        """Handle the 'showmodule' command.

        Calls the appropiate method of searchmodule.

        Args:
            line (str): user-submitted input, may have been auto-completed
        """
        self.searchmodule.showmodule(line)

    def complete_showmodule(self, text, line, begidx, endidx):
        """Handle completion for showmodule.

        To achieve this, the get_categories method of searchmodule is called
        first, which returns our search strings.

        Args:
            text (str): user-submitted keystrokes, used for auto-completion
            line (str): user-submitted input, may have been auto-completed
            begidx (int): beginning index for match
            endidx (int): ending index for match

        Returns:
            List of matches for text

        """
        module_categories = self.searchmodule.get_categories()
        completions = [
            i for i in module_categories if i.startswith(text.lower())
        ]
        return completions

    def help_showmodule(self):
        """Help for showmodule command."""
        print('\nUsage: showmodule [category | all][/modulename]\n')

    def emptyline(self):
        """Handle behaviour for blank input."""
        pass

    def do_exit(self, line):
        """Exit main.

        The return value of True causes Cmd to exit

        Args:
            line (str): user-submitted input
        """
        return True


class SearchModule(object):
    """Handle all module search functionality.

    Called by Main to handle search-related tasks.

    Todo:
        * Look into merging format_category and format_modules table creation
        * Should we pass attributes to methods?
        * We need a few print helpers:
            - Print a single module (should this be the same for show/set?)
            - Print a list of modules (_create_summary_table)
            - Print a category of modules (_create_summary_table)
            - Print all modules (_format_modules)
    """

    def __init__(self):
        """Init method for SearchModule."""
        self.update_index()  # Updates the module index

    def _create_detail_table(self, module_dict):
        """Display detailed module information.

        Args:
            module_dict (dict): Contains module details (author, url, etc.)

        Returns:
            A string containing tabular module details.

        """
        table = texttable.Texttable(max_width=80)  # Create table
        table.set_deco(table.BORDER)               # Set decoration
        table.set_chars(['-', '|', '+', '-'])      # Divider symbols: h,v,c,h
        table.set_cols_align(['r', 'l'])

        for key, value in module_dict.items():
            # TODO: This should come out eventually.
            if key == 'url':
                key = key.upper()
            else:
                key = key.title()

            table.add_row([key, value])
        module_text = '\nModule Details:\n' + table.draw() + '\n'
        return module_text

    def _format_modules(self, module_dict):
        """Display summary of all modules.

        Args:
            module_dict (dict): Full module index ('category': {'module'}).

        Returns:
            A string containing tabular module summary.

        """
        table = texttable.Texttable(max_width=80)  # Create table
        table.set_deco(table.BORDER | table.HLINES)  # Set decoration
        table.set_chars(['-', '|', '+', '-'])  # Divider symbols: h,v,c,h

        for category, modules in module_dict.items():
            for module, details in modules.items():
                table.add_row([module, details['description']])
        module_list = '\n' + table.draw() + '\n'
        return module_list

    def _create_summary_table(self, modules):
        """Display name and description for multiple modules.

        Args:
            modules (array): A list or dict of modules.

        Returns:
            A string containing a table of modules.

        """
        table = texttable.Texttable(max_width=80)  # Create table
        table.set_deco(table.BORDER | table.HLINES)  # Set decoration
        table.set_chars(['-', '|', '+', '-'])  # Divider symbols: h,v,c,h

        if isinstance(modules, list):
            for module in modules:
                module_path = self._format_path(module['role name'],
                                                module['category'])
                table.add_row([module_path, module['description']])

        elif isinstance(modules, dict):
            for key, value in modules.items():
                module_path = self._format_path(value['role name'],
                                                value['category'])
                table.add_row([module_path, value['description']])

        module_table = '\n' + table.draw() + '\n'
        return module_table

    def _format_module_name(self, module_name):
        """Strip spaces and caps from module name for search and display.

        Args:
            module_name (str): Module name

        Returns:
            Module name, minus spaces and caps.

        """
        module_name = module_name.replace(' ', '_').lower()
        return module_name

    def _format_path(self, module, category):
        """Format a module/category for display.

        Args:
            module (str): Module name
            category (str): Category

        Returns:
            Returns the values in 'category/module' format.

        """
        module_name = self._format_module_name(module)
        module_path = f'{category}/{module_name}'
        return module_path

    def update_index(self):
        """Create module index.

        The module index is a dict containing the contents of every module's
        docs.json file, organized by category.

        Example:
            {post-exploitation: {'module1': {'name': 'foo',
                                             'author': 'bar'}},
                                {'module2': {'name': 'foo',
                                             'author': 'bar'}}}

        """
        self.module_index = {}

        # Grab docs.json from all modules in module_dir
        module_docs = module_dir.glob('**/docs.json')

        for doc in module_docs:
            with open(doc, 'r') as d:
                module_dict = json.load(d)
                module_name = self._format_module_name(
                    module_dict['role name'])
                category = module_dict['category']

                if category not in self.module_index:
                    self.module_index[category] = {}

                self.module_index[category][module_name] = module_dict

        # Temporary dump for troubleshooting
        # with open('module_index.json', 'w') as j:
        #     json.dump(self.module_index, j, indent=2)

    def showmodule(self, module):
        """Display information about a given module or modules.

        Depending on the input, either detailed or summary information will be
        returned.

        Args:
            module (str): user-provided input from Main. Should be either all,
            category, or category/module.

        """
        category_module = module.split('/')

        # Either category or 'all' is expected if length is 1
        if len(category_module) == 1:
            category = category_module[0]

            if category == 'all':
                # TODO: Look into moving this to _create_summary_table
                print(self._format_modules(self.module_index))

            # Check for valid category
            elif category in self.module_index.keys():
                category_summary = self._create_summary_table(
                    self.module_index[category])
                print(category_summary)
            else:
                print('Invalid category.')

        # category/module is the expected input at length 2
        elif len(category_module) == 2:
            category = category_module[0]
            module = category_module[1]

            # Check for valid category
            if category in self.module_index.keys():

                # Check for valid module
                if self.module_index[category].get(module):
                    module_dict = self.module_index[category][module]
                    module_detail = self._create_detail_table(module_dict)
                    print(module_detail)
                else:
                    print('Invalid module.')
            else:
                print('Invalid category.')
        else:
            print('wat?')

    def search(self, text):
        """Search modules for string.

        Searches all module text (name, description, author, etc.) for
        provided string.

        Args:
            text (str): user-supplied search term.

        Returns:
            List of matching modules and their descriptions.

        """
        matches = []
        text = text.lower()  # Lower for easier matching

        for category, modules in self.module_index.items():
            for module_name, attributes in modules.items():
                module_name = self._format_module_name(module_name)
                description = attributes['description'].lower()
                if text in category or text in module_name or text in description:
                    matches.append(attributes)
        print('\nSearch Results:\n' + self._create_summary_table(matches))

    def get_categories(self):
        """Create category/module list for searching.

        Input:
            Dict in the category: {module} format

        Returns:
            List of modules in the category/module format.

        """
        category_list = ['all']  # Allow autocomplete of 'all' search option

        for category, modules in self.module_index.items():
            category_list.append(category)  # Allow category autocompletion
            for module_name in modules.keys():
                module_path = self._format_path(module_name, category)
                category_list.append(module_path)
        return category_list


class NewModule(cmd.Cmd, object):
    """Handle new module functionality.

    Called by main when 'newmodule' is invoked. Requires its own Cmd instance
    to support the 'set <value>' autocomplete.

    Todo:
        * Look into yaml module for yml files
          (http://pyyaml.org/wiki/PyYAMLDocumentation)
        * Should self.settings info move to top level
        * Do do_create and _create_dirs need to be separate?
        * Figure out how to fully exit from here (do_exit)

    """

    def __init__(self):
        """Init method for NewModule."""
        cmd.Cmd.__init__(self)  # Initialize the parent
        self.today = date.today().isoformat()

        # Defines the required information for new module
        self.settings = {
            'role name': {
                'name': 'role name',
                'value': '',
                'description': 'Name of your role'
            },
            'role author': {
                'name': 'role author',
                'value': '',
                'description': 'Your name <@yourhandle>'
            },
            'updated': {
                'name': 'updated',
                'value': '',
                'description': 'Date module last updated'
            },
            'category': {
                'name': 'category',
                'value': '',
                'description': 'exploitation, tunnels, etc.'
            },
            'description': {
                'name': 'description',
                'value': '',
                'description': 'A brief (~20-word) description of your module.'
            },
            'instructions': {
                'name': 'instructions',
                'value': '',
                'description': ''
            },
            'url': {
                'name': 'url',
                'value': '',
                'description': 'URL for the original work'
            }
        }

    def format_settings(self, settings_dict):
        """Parse module settings into table.

        Args:
            settings_dict (dict): Dict of dicts containing name, value,
                description keys.

            Example:
                settings_dict = {'module1': {'name': 'module1',
                                             'value': '',
                                             'description': ''},
                                 'module2':  {'name': 'module2',
                                             'value': '',
                                             'description': ''}}

        Returns:
            settings_table (str): Table containing all settings.

        """
        # Create table
        table = texttable.Texttable(max_width=80)

        # Set decoration
        table.set_deco(table.BORDER | table.HEADER | table.VLINES)

        # Divider symbols: h,v,c,h
        table.set_chars(['-', '|', '+', '-'])

        # TODO: Title case
        # # Arbitrary selection here, could be any key

        table.header(settings_dict['role name'].keys())

        for setting, item in settings_dict.items():
            name = item['name'].title()
            value = item['value']
            description = item['description']
            table.add_row([name, value, description])

        settings_table = '\nModule Settings:\n' + table.draw() + '\n'
        return settings_table

    def _set_setting(self, setting, value):
        """Handle modifications to self.settings.

        Args:
            setting (str): Target key in self.settings
            value (str): Value for key

        """
        value = value.replace(f'{setting} ', '')  # Remove setting from value

        self.settings[setting]['value'] = value
        settings_table = self.format_settings(self.settings)
        print(settings_table)  # Print settings after modification

    def _create_dirs(self, name):
        """Create files/directories required for a module.

        Args:
            name (str): name of module

        """
        name = name.replace(' ', '-')  # Replace spaces to avoid messy paths

        # Directories
        role_dir = Path(yams_dir, 'roles', name)  # /roles/<name>
        tasks_dir = Path(role_dir, 'tasks')  # /roles/<name>/tasks

        # File contents
        #   /roles/<name>/tasks/main.yml
        main_yml_content = textwrap.dedent(f"""\
        ---
        - include: {name}.yml
          tags: {name}
        """)

        #  /roles/<name>/tasks/<name>.yml
        name_yml_content = textwrap.dedent(f"""\
        ---
        - name: {name}
        """)

        # Create directories
        #   /roles/<name>
        Path(role_dir).mkdir(parents=True, exist_ok=True)

        #  /roles/<name>/tasks
        Path(tasks_dir).mkdir(parents=True, exist_ok=True)

        # Create files
        #  /roles/<name>/tasks/main.yml
        main_yml_name = Path(tasks_dir, 'main.yml')
        main_yml_name.write_text(main_yml_content)

        #  /roles/<name>/tasks/<name>.yml
        name_yml_name = Path(tasks_dir, f'{name}.yml')
        name_yml_name.write_text(name_yml_content)

        #  /roles/<name>/docs.json
        docs_json_name = Path(role_dir, role_docs_name)
        with open(docs_json_name, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def do_set(self, line):
        """Handle set <setting> input.

        Once line has been supplied, input will be parsed and values set

        Args:
            line (str): user-supplied input

        """
        # TODO: This is ugly. Spaces in keys makes splitting setting/value
        # hard.
        if line.startswith('role name'):
            self._set_setting('role name', line)
        if line.startswith('role author'):
            self._set_setting('role author', line)
        if line.startswith('updated'):
            self._set_setting('updated', line)
        if line.startswith('category'):
            self._set_setting('category', line)
        if line.startswith('description'):
            self._set_setting('description', line)
        if line.startswith('instructions'):
            self._set_setting('instructions', line)
        if line.startswith('url'):
            self._set_setting('url', line)

    def complete_set(self, text, line, begidx, endidx):
        """Handle completion for set.

        Args:
            text (str): user-submitted keystrokes, used for auto-completion
            line (str): user-submitted input, may have been auto-completed
            begidx (int): beginning index for match
            endidx (int): ending index for match

        Returns:
            List of matches for text.

        """
        settings_list = [
            'role name', 'role author', 'updated', 'category', 'description',
            'instructions', 'url'
        ]
        completions = [i for i in settings_list if i.startswith(text.lower())]
        return completions

    def help_set(self):
        """Help for set command."""
        print('\nUsage: set [setting] [value]\n')

    def do_create(self, line):
        """Handle the 'create' command.

        Once invoked, create will write module to disk

        Args:
            line (str): user-supplied input

        """
        self._create_dirs(self.settings['role name'])

    def do_main(self, line):
        """Exit to Main.

        Args:
            line (str): user-supplied input

        Returns:
            True, which causes the NewModule loop to end.

        """
        main.show_main()
        return True

    def do_exit(self, line):
        """Exit YMS.

        Args:
            line (str): user-supplied input

        """
        global exit
        # Exit from YMS, not just NewModule
        exit = True
        return True

    def emptyline(self):
        """Handle behaviour for blank input."""
        pass


if __name__ == '__main__':
    """Handle interactive usage"""

    # Override default completion for OSX
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind('bind ^I rl_complete')
    else:
        readline.parse_and_bind('tab: complete')

    main = Main()
    main.cmdloop()
