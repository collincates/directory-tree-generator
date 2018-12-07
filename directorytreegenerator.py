#!/usr/bin/env python
import errno
import os
import subprocess
import sys
from textwrap import dedent
from itertools import zip_longest

folder_names = {
    'episode_specific': [
        'ADR',
        'As Broadcast Scripts',
        'Cast Deal Memos',
        'Clearance Reports',
        'Closed Captioning',
        'Continuities',
        'Music Cue Sheets',
        'Network Notes',
        'QC Reports',
        'Scripts',
        'Sound Reports',
        'Studio Notes',
        'Timing Sheets',
    ],
    'non_episode_specific': [
        'Budget',
        'Calendars - Post',
        'Calendars - Production',
        'Camera Reports',
        'Cast Lists',
        'Cast Photos',
        'Crew List - Post',
        'Crew List - Production',
        'Deliverables',
        'Distro Lists',
        'Lab Reports',
        'Payroll',
        'Script Supervisor Reports',
        'Start Paperwork',
    ]
}

# Define a decorator that clears the terminal screen before function calls
def clear_screen(function):
    def wrapper(*args, **kwargs):
        os.system('clear')
        function(*args, **kwargs)
    return wrapper


class DirectoryStructure(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.show_name = None
        self.season = None
        self.num_eps = None
        self.cat_folders = []
        self.ep_folders = []

    @clear_screen
    def set_up_show_name(self):
        while True:
            self.show_name = input("\nEnter the name of your show:\t")
            if len(self.show_name) == 0 or self.show_name == ' ':
                print("\nThe show name cannot be blank. Please enter a name for your show:\t")
                continue
            elif any(char in self.show_name for char in ['/', '?', '<', '>', '\\', ':', '*', '|', '"', '\'']):
                print(dedent(
                """
                These characters are not permitted:

                / ? < > \\ : * | ” '
                """
                ), end='')
                continue
            break

    @clear_screen
    def set_up_season_number(self):
        while True:
            try:
                ask_season = int(input("\nWhich season are you in?\t"))
                self.season = f'{ask_season:01}'
                break
            except ValueError:
                print("\nPlease enter a valid season number.")
                continue

    @clear_screen
    def set_up_episode_qty(self):
        while True:
            try:
                ask_eps = int(input("\nHow many episodes are in this season?\t"))
                self.num_eps = [f'{i+1:02}' for i in range(ask_eps)]
                break
            except ValueError:
                print("\nPlease enter a valid number of episodes.")
                continue

    @clear_screen
    def decide_folder_heirarchy(self):
        while True:
            ask_order = input(dedent(
                """
                How do you prefer your folders to be organized?


                Option 1                    Option 2                    Option 3
                ----------------            -----------------           ----------------
                Continuities/               Episode 101/                Continuities/
                    Episode 101/                Continuities/           Scripts/
                    Episode 102/                Scripts/                Timing Sheets/
                    Episode 103/                Timing Sheets/
                Scripts/                    Episode 102/
                    Episode 101/                Continuities/           * Option 3 ignores
                    Episode 102/                Scripts/                 episode number folders
                    Episode 103/                Timing Sheets/
                Timing Sheets/              Episode 103/
                    Episode 101/                Continuities/
                    Episode 102/                Scripts/
                    Episode 103/                Timing Sheets/
                             ...                           ...


                Choose from one of the three options above by typing 1, 2, or 3.

                """
                ))
            if ask_order == '1':
                self.order = 'by_category'
                break
            elif ask_order == '2':
                self.order = 'by_episode'
                break
            elif ask_order == '3':
                self.order = 'category_only'
                break
            else:
                os.system('clear')
                continue

    @clear_screen
    def add_delete_folders(self):
        """User adds and deletes folders from initial folder list."""
        if self.cat_folders:
            categories_used = self.cat_folders
        else:
            categories_used = sorted(
            [folder_name for folders in
            [folder_name for folder_type, folder_name in folder_names.items()]
            for folder_name in folders]
            )
        # while True:
        #     os.system('clear')
        #
        #     # Get list of remaining folders
        #     current_list = list(dict(enumerate(categories_used)).items())
        #
        #     # first_half = current_list[:int(len(current_list) / 2) + 2]
        #     # second_half = current_list[len(first_half):]
        #     # second_half = current_list[int(len(current_list) / 2):]
        #
        #     # Enumerate each folder in terminal view
        #     for one, two in zip_longest(current_list[0:15], current_list[15:], fillvalue='g'):
        #         print(dedent(f'{one[0]}  {one[1]:25}{" ":5}{two[0]}  {two[1]}'))
        #         # print(dedent('{0}  {1}{:10d}{2}  {3}'.format(one[0], one[1], two[0], two[1])))
        #         # print(dedent(f'{one[0]}{one[1]}\t{two[0]}{two[1]}'))
        #         # print(dedent(f'{index + 1}\t{cat}'))
        #
        #     # Accept input to delete folders
        #     try:
        #         ask = int(input())
        #         if ask == 'done':
        #             break
        #         else:
        #             categories_used.pop(ask - 1)
        #     except (ValueError, IndexError):
        #         continue

        self.cat_folders = categories_used

    @clear_screen
    def confirm_layout(self):
        while True:
            """Display confirmation page showing current directory structure."""

            print(dedent(
            """

            Below is a list of folders that will be included:
            --------------------------------------------------------
            """
            ))
            ### FIGURE OUT HOW TO SORT NAMES BEFORE SPLITTING INTO TWO EQUAL COLUMNS ###
            for one, two in zip_longest(folder_names['episode_specific'], folder_names['non_episode_specific'], fillvalue=''):
            # for one, two in zip_longest(self.cat_folders[:14], self.cat_folders[14:], fillvalue=''):
                print(one.ljust(30), two)

            print(dedent(
            """
            --------------------------------------------------------
            SAVE            to confirm the list
            EDIT            to make changes
            START OVER      to scrap everything and start over
            """
            ))

            # Ask user to confirm, edit, or start over
            ask_confirm = input("Type SAVE, EDIT, or START OVER: ")

            if ask_confirm.lower() == 'save':
                self.create_directory_tree()
                break
            elif ask_confirm.lower() == 'edit':
                print("Edit page not yet implemented.")
                ### IMPLEMENT THIS ###
                # self.add_delete_folders()
                continue
            elif ask_confirm.lower() == 'start over':
                # Reset instance variables of DirectoryStructure and start over
                print("Edit page not yet implemented.")
                ### IMPLEMENT THIS ###
                # self.reset()
                # self.main()
                continue

    def create_directory_tree(self, open_in_finder=True):

        print('Starting directory tree build...')

        # Concatenate season number with episode number as a list of strings
        # e.g. ['Episode 101', 'Episode 102', 'Episode 103']
        self.ep_folders = [f'Episode {self.season}{ep}' for ep in self.num_eps]

        # Define absolute path for show's root directory
        show_root = os.path.join(os.getcwd(), self.show_name, '')

        # make_dirs_in_cwd_from() builds a nested directory structure
        # in current working directory with dir names as parameters (strings)
        #
        # e.g. make_dirs_in_cwd_from('sub1', 'sub2', 'sub3')   makes:
        #      ../
        #          ./
        #             sub1/
        #                 sub2/
        #                     sub3/
        def make_dirs_in_cwd_from(*args):
            return os.makedirs(os.path.join(os.getcwd(), *args, ''), exist_ok=True)

        # Make show's root directory from absolute path saved in show_root
        if not os.path.exists(show_root):
            try:
                # os.makedirs(value, 0o700)
                os.mkdir(show_root)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        # Make all episode-specific folders
        for cat in folder_names['episode_specific']:
            for ep in self.ep_folders:
                # Organize subdirectories as show_name/category/episodes/
                if self.order == 'by_category':
                    make_dirs_in_cwd_from(show_root, cat, ep)
                # Organize subdirectories as show_name/episodes/category/
                elif self.order == 'by_episode':
                    make_dirs_in_cwd_from(show_root, ep, cat)
                # Organize subdirectories as show_name/category/ without episodes
                else:
                # elif self.order == 'category_only':
                    make_dirs_in_cwd_from(show_root, cat)

        # Make all non-episode-specific folders
        for cat in folder_names['non_episode_specific']:
            make_dirs_in_cwd_from(show_root, cat)

        os.system('clear')
        print(dedent(
        f"""
        Build successful!





        Your new project folder can be found at:

        {'-' * len(os.path.join(os.getcwd(), self.show_name, ''))}
        {os.path.join(os.getcwd(), self.show_name, '')}
        {'-' * len(os.path.join(os.getcwd(), self.show_name, ''))}





        (You can close this window now.)





        """
        ))

        # Open new project folder in Finder if open_in_finder == True
        if open_in_finder == True:
            subprocess.call(['open', '-R', os.path.join(os.getcwd(), self.show_name)])

    def main(self):
        self.set_up_show_name()
        self.set_up_season_number()
        self.set_up_episode_qty()
        self.decide_folder_heirarchy()
        # self.add_delete_folders() # This is still under construction
        self.confirm_layout()
        # self.create_directory_tree() # Moved to 'save' clause in confirm_layout()


if __name__=="__main__":
    wizard = DirectoryStructure()
    wizard.main()
