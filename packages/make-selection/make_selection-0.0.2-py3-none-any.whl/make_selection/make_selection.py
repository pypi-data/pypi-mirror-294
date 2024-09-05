"""
Module for interactive command line menu. Simply accepts a list of str-able objects
and allows user to select using arrow keys.
"""
import sys
if sys.platform != "win32":
    raise NotImplementedError("This module is only available on Windows.")
from typing import Any
import msvcrt
import ctypes

stdout = -11
enable_ansi_codes = 7
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(stdout), enable_ansi_codes)

ANSI_MOVE_CURSOR = "\x1b[{up}F\r\x1b[{right}C"
ANSI_HIGHLIGHT   = "\x1b[30;47m"
ANSI_YELLOW      = "\x1b[93m"
ANSI_BLUE        = "\x1b[94m"
ANSI_RESET       = "\x1b[0m"
SPECIAL_KEY = 224
UP_ARROW    = 72
DOWN_ARROW  = 80
ENTER_KEY   = 13
CTL_C       = 3
BACKSPACE   = 8
SPACEBAR    = 32

class Menu:
    def __init__(self, options: list, label: str, window_size: int=10) -> None:
        assert options
        assert label
        assert 1 <= window_size
        window_size = min((len(options)), window_size)

        self.options_original = options
        self.options_current = options
        self.search_indices = []
        self.search_string = ""
        self.label = label
        self.selected_index = 0
        self.window_top = 0
        self.window_size_original = window_size
        self.window_size_current = window_size
        self.help_string = "Enter: Select, Ctl+C: Cancel"

    def show(self):
        print(f"{ANSI_BLUE}{self.label}>{ANSI_RESET}")
        self.printMenu()
        while True:
            something_changed = False
            char = self.getChar()
            if char == SPECIAL_KEY:
                char = self.getChar()
                if 1 < len(self.options_current):
                    # Update selected index
                    if char == UP_ARROW:
                        self.selected_index = (self.selected_index - 1) % len(self.options_current)
                        something_changed = True
                    elif char == DOWN_ARROW:
                        self.selected_index = (self.selected_index + 1) % len(self.options_current)
                        something_changed = True
                
                    # Update window
                    if something_changed:
                        bottom = self.window_top + self.window_size_current
                        if self.selected_index < self.window_top:
                            self.window_top = self.selected_index
                        elif bottom <= self.selected_index:
                            self.window_top = self.selected_index - self.window_size_current + 1
            elif self.isSearchableChar(char):
                char = chr(char)
                self.search_string = f"{self.search_string}{char}".lstrip()
                if self.search_string:
                    print(char, end="", flush=True)
                    self.search(self.options_current)
                    something_changed = True
            elif char == BACKSPACE and 0 < len(self.search_string):
                self.search_string = self.search_string[:-1]
                # Move left, print space, move left again
                print("\x1b[1D \x1b[1D", end="", flush=True)
                self.search(self.options_original)
                something_changed = True
            elif char == ENTER_KEY and self.options_current:
                self.printSelected()
                return self.options_current[self.selected_index]
            elif char == CTL_C:
                self.clearMenu(clear_label=True)
                print("cancelled")
                return None

            if something_changed:
                self.clearMenu()
                self.printMenu()

    def search(self, search_list: list) -> None:
        found_indices = []
        found_options = []
        for o in search_list:
            found_i = str(o).lower().find(self.search_string.lower())
            if found_i != -1:
                found_indices.append(found_i)
                found_options.append(o)
        self.options_current = found_options
        self.search_indices = found_indices

        # Reset window after modifying options
        self.window_top = 0
        self.selected_index = 0
        self.window_size_current = min((len(self.options_current), self.window_size_original))
    
    def getChar(self) -> int:
        return ord(msvcrt.getch())

    def isSearchableChar(self, char):
        return (32 <= char and char <= 126)
    
    def clearMenu(self, clear_label=False):
        if clear_label:
            print("\x1b[0G\x1b[J", end="", flush=True)
        else:
            print("\x1b[J")

    def printMenu(self):
        bottom = self.window_top + self.window_size_current
        if not self.options_current:
            print(f"{ANSI_BLUE}no matches found{ANSI_RESET}")
            # NOTE: window size is 0 here after empty search, but we are printing 1 line
            #       so we need to set it so the footer prints correctly
            self.window_size_current = 1
        else:
            for i in range(self.window_top, bottom):
                if i == self.selected_index:
                    print(f"{ANSI_HIGHLIGHT}{self.options_current[i]}{ANSI_RESET}")
                else:
                    print(self.options_current[i])
        print(f"{ANSI_YELLOW}{self.help_string}{ANSI_RESET}\n{ANSI_MOVE_CURSOR.format(up=self.window_size_current + 2, right=len(self.label) + len(self.search_string) + 1)}", end="", flush=True)

    def printSelected(self):
        self.clearMenu(clear_label=True)
        print(f"{self.label}> {self.options_current[self.selected_index]}")

def makeSelection(options: list[Any], label: str, window_size: int=None) -> Any:
    """
    Entry point for menu selection.

    Parameters
    ----------
    options
        List of str-able objects.
    label
        Label to describe the items being selected.
    window_size
        Max number of items to show at once.

    Returns
    -------
    Selected value.
    """
    if window_size:
       return Menu(options, label, window_size).show()
    else:
       return Menu(options, label).show()

if __name__ == "__main__":
    print(f"Returns: '{makeSelection(['interactive', 'cli', 'menu'], 'make_selection')}'")