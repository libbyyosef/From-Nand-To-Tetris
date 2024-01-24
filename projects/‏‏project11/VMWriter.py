"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

LOCAL = "local"
CONST = "const"
ARG = "arg"
STATIC = "static"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"
PUSH = "push"
POP="pop"


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """

        self.output_stream.write(PUSH + " " + segment + " " +
                                 index.__str__()+"\n")


    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG",
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        self.output_stream.write(POP + " " + segment + " " + index.__str__()+"\n")


    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG",
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        self.output_stream.write(command+"\n")



    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        self.output_stream.write("label "+label+"\n")


    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write("goto " + label+"\n")


    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write("if-goto " + label+"\n")


    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        self.output_stream.write("call " +name+" "+n_args.__str__()+"\n")


    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        self.output_stream.write("function "+name+" "+n_locals.__str__()+"\n")


    def write_return(self) -> None:
        """Writes a VM return command."""
        self.output_stream.write("return\n")

    def handle_const_str(self,string):
        string_length=len(string)
        self.write_push("constant",string_length)
        self.write_call("String.new",1)
        i=0
        while i<string_length:
            c:str=string[i]
            self.write_push("constant",ord(c))
            self.write_call("String.appendChar",2)
            i+=1

