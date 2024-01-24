"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"



class Parser:
    """
    # Parser

    Handles the parsing of a single .vm file, and encapsulates access to
    the
    input code. It reads VM commands, parses them, and provides convenient
    access to their components.
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly
    commands. VM commands may be separated by an arbitrary number of
    whitespace
    characters and comments, which are ignored. Comments begin with "//"
    and
    last until the line’s end.
    The different parts of each VM command may also be separated by an
    arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this,
      that,
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.__input_lines = input_file.read().splitlines()
        self.__num_of_line = 0
        self.__current_line = self.__input_lines[self.__num_of_line]
        self.__num_of_words = 0
        self.__static_counter=0
        self.__arg0=""
        self.__arg1=""
        self.__arg2=""

        self.__current_cmd_type = self.cmd_type_helper(self.arg1())

    @staticmethod
    def cmd_type_helper(arg1):
        dict_commands_type = {"add": C_ARITHMETIC, "sub": C_ARITHMETIC,
                              "neg": C_ARITHMETIC, "eq": C_ARITHMETIC,
                              "gt": C_ARITHMETIC, "lt": C_ARITHMETIC,
                              "and": C_ARITHMETIC, "or": C_ARITHMETIC,
                              "not": C_ARITHMETIC, "push": C_PUSH,
                              "pop": C_POP, "shiftleft":C_ARITHMETIC,
                              "shiftright":C_ARITHMETIC,"label":C_LABEL,
                              "if-goto":C_IF, "goto":C_GOTO,
                              "function":C_FUNCTION, "call":C_CALL,
                              "return":C_RETURN}

        return dict_commands_type[arg1] if arg1 in dict_commands_type else None

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self.__num_of_line != len(self.__input_lines)

    def init_update_args_cmt_type(self):
        self.split_to_args()
        self.__current_cmd_type = self.cmd_type_helper(self.__arg1)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true.
        Initially
        there is no current command.
        """
        # Your code goes here!

        # only if there are more cmds

        # while self.__current_cmd_type is None and self.has_more_commands():
        self.__num_of_line += 1
        if self.has_more_commands():
            self.__current_line = self.__input_lines[self.__num_of_line]
            self.init_update_args_cmt_type()




    def split_to_args(self):
        slesh=self.__current_line.find("/")
        slesh1=self.__current_line.find("\\")

        if slesh!=-1:
            self.__current_line=self.__current_line[:slesh]
        if slesh1!=-1:
            self.__current_line = self.__current_line[:slesh1]



        list_replace=self.__current_line.replace(';',' ')
        list_replace=list_replace.replace(" ","!")
        words_split_list=list_replace.split("!")
        temp_list=[]
        for val in words_split_list:
            if val !='' and len(val)!=0:
                temp_list.append(val)


        #
        # if temp_list is None:
        #     self.__arg0 = ""
        #     self.__arg1 = ""
        #     self.__arg2 = ""
        if len(temp_list)==0:
            self.__arg0 = ""
            self.__arg1 =""
            self.__arg2 = ""
        if len(temp_list)==1:
            self.__arg0 = ""
            self.__arg1 = temp_list[0]
            self.__arg2 = ""


        elif len(temp_list)==2:
            self.__arg0 = temp_list[1]
            # label name
            self.__arg1 = temp_list[0]
            self.__arg2=""

        elif len(temp_list)==3:
            self.__arg0 = temp_list[1]
            #conatant, pointer, that this and so..
            self.__arg1 = temp_list[0]
            self.__arg2 = temp_list[2]



    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        return self.__current_cmd_type

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of
            "C_ARITHMETIC", the command itself (add, sub, etc.) is
            returned.
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!

        return self.__arg1

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP",
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!

        #if self.__current_cmd_type in {C_PUSH, C_POP, C_FUNCTION, C_CALL}:


        return int(self.__arg2)

    def arg0(self) -> str:
        return self.__arg0

    def memory_place(self) -> str:
        return self.__arg0

    # def get_file_name(self):
    #     return self.__
