"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

A_COMMAND = "A_COMMAND"
L_COMMAND = "L_COMMAND"
C_COMMAND = "C_COMMAND"
A_SIGN = '@'
LABEL_SIGN = '('


class Parser:
    """Encapsulates access to the input code. Reads an assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()
        self.num_of_current_line = 0
        self.input_lines = input_file.read().splitlines()
        self.type_instruction = "None"
        self.current_line = self.input_lines[self.num_of_current_line]
        self.start_line=0
        self.check_start_line=False

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return len(self.input_lines) != (self.num_of_current_line)

    def advance_helper(self, counter):
        self.num_of_current_line += 1
        if self.type_instruction != 'None'and counter==1:
            self.start_line=self.num_of_current_line
            self.check_start_line=True
        if self.has_more_commands():
            self.current_line = self.input_lines[
                self.num_of_current_line].replace(" ","")
            self.update_type_instruction()

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current
        command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        counter=1
        skip_part2 = False
        while self.command_type() not in [A_COMMAND, L_COMMAND, C_COMMAND]:
            skip_part2 = True
            if self.check_start_line:
                counter+=1
            self.advance_helper(counter)
        if not skip_part2:
            if self.check_start_line:
                counter+=1
            self.advance_helper(counter)

    def update_type_instruction(self) -> None:
        idx=0
        if len(self.current_line)>0:
            first_char = self.current_line[idx]
            while first_char == " ":
                idx+=1
                if idx==len(self.current_line):
                    break
                first_char = self.current_line[idx]
            if first_char == A_SIGN:
                self.type_instruction = "A_COMMAND"
            elif first_char == LABEL_SIGN:
                self.type_instruction = "L_COMMAND"
            elif first_char == "D" or first_char == "A" or first_char == "M" \
                    or first_char == '0':
                self.type_instruction = "C_COMMAND"
            else:
                self.type_instruction = "None"
        else:
            self.type_instruction = "None"

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal
            number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a
            symbol
        """
        # Your code goes here!

        return self.type_instruction

    def read_all_over_again(self) -> None:
        self.num_of_current_line = 0
        self.current_line = self.input_lines[self.num_of_current_line]
        self.update_type_instruction()

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # Your code goes here!
        if self.type_instruction == A_COMMAND:
            str_symbol = self.current_line[self.current_line.find(A_SIGN) + 1:]
            return str_symbol.replace(" ","")
        elif self.type_instruction == L_COMMAND:
            str_symbol = self.current_line[self.current_line.find("(") +
                                           1:self.current_line.find(")")]

            return str_symbol.replace(" ","")

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.type_instruction == C_COMMAND:
            slesh = self.current_line.find('/')
            if self.current_line.find("=") == -1:
                return "null"
            else:
                if slesh==-1:
                    return self.current_line[:self.current_line.find("=")].replace(" ","")
                elif slesh<self.current_line.find("="):
                    return "null"
                else:
                    return self.current_line[:self.current_line.find("=")].replace(" ","")






    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.type_instruction == C_COMMAND:

            start = self.current_line.find("=") + 1
            slesh=self.current_line.find(
                    '/')
            if self.current_line.find(";") == -1 :
                if slesh==-1:
                    return self.current_line[start:].replace(" ","")
                else:
                    return self.current_line[start:slesh].replace(" ","")
            else:
                if slesh==-1:
                    return self.current_line[start:self.current_line.find(
                        ";")].replace(" ","")
                elif self.current_line.find('/') < self.current_line.find(";"):
                    return self.current_line[start:slesh].replace(" ","")
                else:
                    return self.current_line[start:self.current_line.find(
                        ";")].replace(" ","")


    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.type_instruction == C_COMMAND:
            if self.current_line in ["A;","D;","M;"] :
                return "null";

            slesh = self.current_line.find('/')
            if self.current_line.find(";") == -1:
                    return "null"
            else:
                if slesh==-1:
                    return self.current_line[self.current_line.find(";") + 1:].replace(" ","")
                elif slesh<self.current_line.find(";"):
                    return "null"
                else:
                  return self.current_line[self.current_line.find(";") +
                                           1:slesh].replace(" ","")


