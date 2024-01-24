"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import  os

START_CODE = "    @SP\n    M=M-1\n    "
C_PUSH = "C_PUSH"
C_POP="C_POP"
SHIFTLEFT="    @SP\n    A=M-1\n    M=M<<\n"
SHIFTRIGHT="    @SP\n    A=M-1\n    M=M>>\n"
PUSH_TEMP="    @5\n    D=A\n    @num\n    D=D+A\n    A=D\n    D=M\n    @SP\n    A=M\n    " \
          "M=D\n    @SP\n    M=M+1\n"
POP_STATIC="    @SP\n    M=M-1\n    A=M\n    D=M\n    @Foo.num\n    M=D\n"
PUSH_STATIC="    @Foo.num\n    D=M\n    @SP\n    A=M\n    M=D\n    @SP\n    " \
            "M=M+1\n"
POP_POINTER="    @SP\n    M=M-1\n    A=M\n    D=M\n    @THIS\n    M=D\n"
PUSH_POINTER="    @THIS\n    D=M\n    @SP\n    A=M\n    M=D\n    @SP\n    " \
             "M=M+1\n"
POP_TEMP="    @SP\n    M=M-1\n    A=M\n    D=M\n    @R13\n    " \
         "M=D\n    @5\n    D=A\n    @num\n    D=D+A\n    @R14\n    M=D\n    " \
         "@R13\n    D=M\n    @R14\n    A=M\n    M=D\n"
POP_CODE="    @SP\n    M=M-1\n    A=M\n    D=M\n    @R13\n    " \
         "M=D\n    @LCL\n    D=M\n    @num\n    D=D+A\n    @R14\n    M=D\n    " \
         "@R13\n    D=M\n    @R14\n    A=M\n    M=D\n"
PUSH_LOCAL="    @LCL\n    D=M\n    @num\n    D=D+A\n    A=D\n    D=M\n    " \
           "@SP\n    A=M\n    M=D\n    @SP\n    M=M+1\n"
PUSH_CODE="    D=A\n    @SP\n    A=M\n    M=D\n    @SP\n    M=M+1\n"
ADD_CODE = "    @SP\n    A=M-1\n    D=M\n    A=A-1\n    " \
           f"M=D+M\n    @SP\n    M=M-1\n"
SUB_CODE = "    @SP\n    M=M-1\n    A=M-1\n    D=M\n    A=A+1\n    D=D-M\n   " \
           " @SP\n    M=M-1\n    A=M\n    M=D\n    @SP\n    M=M+1\n"
NEG_CODE = "    @SP\n    A=M-1\n    M=-M\n"
EQ_CODE1 = "A=M\n    D=M\n    A=A-1\n    D=D-M\n    @VAL_EQ"
EQ_CODE2 = "\n    D;JEQ\n    @SP\n    A=M-1\n    M=0\n    @VAL_NO_EQ"
EQ_CODE_NO = "\n    0;JMP\n(VAL_EQ"
EQ_CODE3 = ")\n    @SP\n    A=M-1\n    M=-1\n(VAL_NO_EQ"
EQ_CODE_NO1 = ")\n"

# GT_CODE1 = "A=M\n    D=M\n    A=A-1\n    D=D-M\n    @VAL_GT"
# GT_CODE2 = "\n    D;JLT\n    @SP\n    A=M-1\n    M=0\n    @VAL_NO_GT"
# GT_CODE_NO = "\n    0;JMP\n(VAL_GT"
# GT_CODE3 = ")\n    @SP\n    A=M-1\n    M=-1\n(VAL_NO_GT"
# GT_CODE_NO1 = ")\n"


GT_CODE1 = "A=M-1\n    D=M\n    @first_val\n    M=-1\n    @UPDATE_VAL"
GT_CODE_2="\n    D;JGE\n    @PASS"
GT_CODE_3="\n    0;JMP\n(UPDATE_VAL"
GT_CODE_4=")\n    @first_val\n    M=1\n(PASS"
GT_CODE_5=")\n    @SP\n    A=M\n    D=M\n    @second_val\n    M=-1\n    " \
          "@UPDATE_VALUE"
GT_CODE_6="\n    D;JGE\n    @PASS0"
GT_CODE_7="\n    0;JMP\n(UPDATE_VALUE"
GT_CODE_8=")\n    @second_val\n    M=1\n(PASS0"
GT_CODE_9=")\n    @first_val\n    D=M\n    @second_val\n    D=D+M\n    @EDGE"
GT_CODE_10="\n    D;JEQ\n    @SP\n    M=M-1\n    A=M\n    D=M\n    " \
          "A=A+1\n    D=D-M\n    @IS_GT"
GT_CODE_11="\n    D;JGT\n    @SP\n    A=M\n    " \
          "M=0\n    @SP\n    M=M+1\n    @END"
GT_CODE_12="\n    0;JMP\n(IS_GT"
GT_CODE_13=")\n    @SP\n    A=M\n    M=-1\n    @SP\n    M=M+1\n    @END"
GT_CODE113="\n    0;JMP\n"
GT_CODE_14="(EDGE"
GT_CODE_15=")\n    @first_val\n    D=M\n    @CORRECT"
GT_CODE_16="\n    D;JGT\n    @SP\n    M=M-1\n    A=M\n    M=0\n    @SP\n    " \
           "M=M+1\n    @END"
GT_CODE_17="\n    0;JMP\n(CORRECT"
GT_CODE_18=")\n    @SP\n    M=M-1\n    A=M\n    M=-1\n    @SP\n    M=M+1\n(END"
GT_CODE_19=")\n"

# LT_CODE1 = "A=M\n    D=M\n    A=A-1\n    D=D-M\n    @VAL_LT"
# LT_CODE2 = "\n    D;JGT\n    @SP\n    A=M-1\n    M=0\n    @VAL_NO_LT"
# LT_NO_CODE = "\n    0;JMP\n(VAL_LT"
# LT_CODE3 = ")\n    @SP\n    A=M-1\n    M=-1\n(VAL_NO_LT"
# LT_CODE_NO1 = ")\n"

LT_CODE1 = "A=M-1\n    D=M\n    @first_val\n    M=-1\n    @UPDATE_VAL"
LT_CODE_2="\n    D;JGE\n    @PASS"
LT_CODE_3="\n    0;JMP\n(UPDATE_VAL"
LT_CODE_4=")\n    @first_val\n    M=1\n(PASS"
LT_CODE_5=")\n    @SP\n    A=M\n    D=M\n    @second_val\n    M=-1\n    " \
          "@UPDATE_VALUE"
LT_CODE_6="\n    D;JGE\n    @PASS0"
LT_CODE_7="\n    0;JMP\n(UPDATE_VALUE"
LT_CODE_8=")\n    @second_val\n    M=1\n(PASS0"
LT_CODE_9=")\n    @first_val\n    D=M\n    @second_val\n    D=D+M\n    @EDGE"
LT_CODE_10="\n    D;JEQ\n    @SP\n    M=M-1\n    A=M\n    D=M\n    " \
          "A=A+1\n    D=D-M\n    @IS_LT"
LT_CODE_11="\n    D;JLT\n    @SP\n    A=M\n    " \
          "M=0\n    @SP\n    M=M+1\n    @END"
LT_CODE_12="\n    0;JMP\n(IS_LT"
LT_CODE_13=")\n    @SP\n    A=M\n    M=-1\n    @SP\n    M=M+1\n    @END"
LT_CODE113="\n    0;JMP\n"
LT_CODE_14="(EDGE"
LT_CODE_15=")\n    @first_val\n    D=M\n    @CORRECT"
LT_CODE_16="\n    D;JLT\n    @SP\n    M=M-1\n    A=M\n    M=0\n    @SP\n    " \
           "M=M+1\n    @END"
LT_CODE_17="\n    0;JMP\n(CORRECT"
LT_CODE_18=")\n    @SP\n    M=M-1\n    A=M\n    M=-1\n    @SP\n    M=M+1\n(END"
LT_CODE_19=")\n"



AND_CODE1 = "A=M\n    D=M\n    A=A-1\n    M=D&M\n"

OR_CODE1 = "A=M\n    D=M\n    A=A-1\n    M=D|M\n"

NOT_CODE1 = "    @SP\n    A=M-1\n    M=!M\n"




class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.__output_stream = output_stream
        self.__file_name = os.path.basename(output_stream.name)
        self.__counter = 0
        self.__val_in_sp = 256

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions
        # between two
        # .vm files which push/pop to the static segment, one can use the
        # current
        # file's name in the assembly variable's name and thus differentiate
        # between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(
        # os.path.basename(input_file.name))
        self.__file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        lt_val=START_CODE+LT_CODE1 + f"{self.__counter}" + LT_CODE_2 +\
              f"{self.__counter}" + LT_CODE_3 + f"{self.__counter}" \
               +LT_CODE_4 + f"{self.__counter}"+ LT_CODE_5 + f"{self.__counter}"+ \
                LT_CODE_6 + f"{self.__counter}"+ LT_CODE_7 + f"{self.__counter}"+\
                LT_CODE_8 + f"{self.__counter}"+ LT_CODE_9 + f"{self.__counter}"+\
                LT_CODE_10 +f"{self.__counter}"+ LT_CODE_11 +f"{self.__counter}"\
               + LT_CODE_12+f"{self.__counter}" + LT_CODE_13+f"{self.__counter}"+\
               LT_CODE113+ LT_CODE_14 + f"{self.__counter}" + LT_CODE_15+\
                f"{self.__counter}"\
               + LT_CODE_16+f"{self.__counter}" + LT_CODE_17+f"{self.__counter}"\
               + LT_CODE_18 + f"{self.__counter}" + LT_CODE_19

        gt_val = START_CODE + GT_CODE1 + f"{self.__counter}" + GT_CODE_2 + \
                 f"{self.__counter}" + GT_CODE_3 + f"{self.__counter}" \
                 + GT_CODE_4 + f"{self.__counter}" + GT_CODE_5 + f"{self.__counter}" + \
                 GT_CODE_6 + f"{self.__counter}" + GT_CODE_7 + f"{self.__counter}" + \
                 GT_CODE_8 + f"{self.__counter}" + GT_CODE_9 + f"{self.__counter}" + \
                 GT_CODE_10 + f"{self.__counter}" + GT_CODE_11 + f"{self.__counter}" \
                 + GT_CODE_12 + f"{self.__counter}" + GT_CODE_13 + f"{self.__counter}" + \
                 GT_CODE113+ GT_CODE_14 + f"{self.__counter}" + GT_CODE_15 + f"{self.__counter}" \
                 + GT_CODE_16 + f"{self.__counter}" + GT_CODE_17 + f"{self.__counter}" \
                 + GT_CODE_18 + f"{self.__counter}" + GT_CODE_19




        dict_arithmetic = {"add": ADD_CODE, "sub": SUB_CODE, "neg": NEG_CODE,
                           "eq": START_CODE + EQ_CODE1 + f"{self.__counter}" +
                                 EQ_CODE2 + f"{self.__counter}" + EQ_CODE_NO
                                 + f"{self.__counter}" + EQ_CODE3 + f"{self.__counter}"
                                 + EQ_CODE_NO1,
                           "gt": gt_val,

                           "lt": lt_val,
                           "and": START_CODE + AND_CODE1 ,
                           "or": START_CODE + OR_CODE1 ,
                           "not": NOT_CODE1, "<<":SHIFTLEFT,
                           ">>":SHIFTRIGHT }
        self.__counter += 1
        self.__output_stream.write(dict_arithmetic[command])

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm
        # should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.

        if command == "push" :
            # change val according to segment
            new_push_code=PUSH_LOCAL.replace("num",f"{index}")
            if segment == "constant":
                self.__output_stream.write(
                    f"    @{index}\n" + PUSH_CODE)
            elif segment=="local":
                self.__output_stream.write(new_push_code)
            elif segment=="argument":
                self.__output_stream.write(new_push_code.replace("LCL","ARG"))
            elif segment=="this":
                self.__output_stream.write(new_push_code.replace("LCL","THIS"))
            elif segment == "that":
                self.__output_stream.write(new_push_code.replace("LCL", "THAT"))
            elif segment == "temp":
                self.__output_stream.write(PUSH_TEMP.replace("num", f"{index}"))
            elif segment == "pointer":
                if index==0:
                    self.__output_stream.write(PUSH_POINTER)
                elif index==1:
                    self.__output_stream.write(PUSH_POINTER.replace("THIS", "THAT"))
            elif segment == "static":
                new_push_static=PUSH_STATIC.replace("num",f"{index}")
                self.__output_stream.write(new_push_static.replace("Foo",
                                                                   self.__file_name[:-4]))

        elif command=="pop":
            new_pop_code=POP_CODE.replace("num", f"{index}")
            if segment=="local":
                self.__output_stream.write(new_pop_code)
            elif segment=="argument":
                self.__output_stream.write(new_pop_code.replace("LCL","ARG"))
            elif segment == "this":
                self.__output_stream.write(new_pop_code.replace("LCL", "THIS"))
            elif segment == "that":
                self.__output_stream.write(new_pop_code.replace("LCL", "THAT"))
            elif segment == "temp":
                self.__output_stream.write(POP_TEMP.replace("num", f"{index}"))
            elif segment == "pointer":
                if index == 0:
                    self.__output_stream.write(POP_POINTER)
                elif index == 1:
                    self.__output_stream.write(POP_POINTER.replace("THIS", "THAT"))
            elif segment == "static":
                new_pop_static = POP_STATIC.replace("num", f"{index}")
                self.__output_stream.write(new_pop_static.replace("Foo",
                                                              self.__file_name[:-4]))

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the
        symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the
        # code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp
        # var
        # *ARG = pop()                  // repositions the return value for
        # the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
