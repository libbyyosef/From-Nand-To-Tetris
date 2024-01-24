"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code

A_COMMAND = "A_COMMAND"
L_COMMAND = "L_COMMAND"
C_COMMAND = "C_COMMAND"


class HackAssembler:
    def __init__(self, input_file1, output_file1):
        self.parser: Parser = Parser(input_file1)
        self.symbol_table: SymbolTable = SymbolTable()
        self.input_file = input_file1
        self.output_file = output_file1
        self.address = 16
        self.nm_l_commands_2_reading=0

    def first_reading(self):
        while self.parser.has_more_commands():
            self.parser.advance()
            if self.parser.command_type() == L_COMMAND:
                self.nm_l_commands_2_reading += 1
                self.symbol_table.add_entry(self.parser.symbol(),
                                            self.parser.num_of_current_line-self.parser.start_line
                                            + 2-self.nm_l_commands_2_reading)
                # self.address += 1
                # if self.address == self.symbol_table.table["SCREEN"] or \
                #         self.address == self.symbol_table.table["KBD"]:
                #     self.address += 1
            # self.parser.advance()


    def specific_address(self,address:str)->bool:
        for char in address[1:]:
            if char not in ['0','1','2','3','4','5','6','7','8','9']:
                return False
        return True




    def second_reading(self):
        self.parser.read_all_over_again()
        while self.parser.has_more_commands():
            if self.parser.type_instruction == A_COMMAND :

                symb = self.parser.symbol()
                range1= [str(x) for x in range(16)]
                if not self.symbol_table.contains(symb) and symb not in range1:
                    if not self.specific_address(symb):
                        self.output_file.write(format(self.address, '016b') + "\n")
                        self.symbol_table.add_entry(self.parser.symbol(),
                                                    self.address)
                        self.address += 1
                    else:
                        self.output_file.write(
                            format(int(symb), '016b') + "\n")
                        self.symbol_table.add_entry(self.parser.symbol(),
                                                    int(symb))

                    if self.address == self.symbol_table.table["SCREEN"] \
                            or \
                            self.address == self.symbol_table.table["KBD"]:
                        self.address += 1
                else:
                    if self.symbol_table.contains(symb):
                        out=format(self.symbol_table.table[
                                                      symb], '016b') + "\n"
                        self.output_file.write(out)
                    else:
                        self.output_file.write(format(self.symbol_table.table[
                                                          'R'+symb],
                                                      '016b') + "\n")


                self.parser.advance()
                """parsing to binary"""
            elif self.parser.type_instruction == C_COMMAND:
                destination = self.parser.dest()
                cmp = self.parser.comp()
                jmp = self.parser.jump()
                if jmp=='':
                    jmp="null";
                pre = "111"
                if '<<' in cmp or '>>' in cmp:
                    pre="101"
                dest_binary = Code.dest(destination)
                comp_binary = Code.comp(cmp)
                jump_binary = Code.jump(jmp)
                inst = comp_binary + dest_binary + jump_binary
                binary_instruction = pre + inst
                self.output_file.write(binary_instruction + "\n")
                self.parser.advance()
            else:
                self.parser.advance()

    def binary(self, s):
        return "{0:b}".format(int(s))


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    """
    You should use the two-pass implementation suggested in the book:
    
    *Initialization*
    Initialize the symbol table with all the predefined symbols and their
    pre-allocated RAM addresses, according to section 6.2.3 of the book.
    
    *First Pass*
    Go through the entire assembly program, line by line, and build the symbol
    table without generating any code. As you march through the program lines,
    keep a running number recording the ROM address into which the current
    command will be eventually loaded.
    This number starts at 0 and is incremented by 1 whenever a C-instruction
    or an A-instruction is encountered, but does not change when a label
    pseudo-command or a comment is encountered. Each time a pseudo-command
    (Xxx) is encountered, add a new entry to the symbol table, associating
    Xxx with the ROM address that will eventually store the next command in
    the program.
    This pass results in entering all the program’s labels along with their
    ROM addresses into the symbol table.
    The program’s variables are handled in the second pass.
    
    *Second Pass*
    Now go again through the entire program, and parse each line.
    Each time a symbolic A-instruction is encountered, namely, @Xxx where Xxx
    is a symbol and not a number, look up Xxx in the symbol table.
    If the symbol is found in the table, replace it with its numeric meaning
    and complete the command’s translation.
    If the symbol is not found in the table, then it must represent a new
    variable. To handle it, add the pair (Xxx,n) to the symbol table, where n
    is the next available RAM address, and complete the command’s translation.
    The allocated RAM addresses are consecutive numbers, starting at address
    16 (just after the addresses allocated to the predefined symbols).
    After the command is translated, write the translation to the output file.
    
    Tools:
    Two useful tools are the supplied Assembler and the supplied CPU
    Emulator, both available in your tools directory. These tools allow
    experimenting with a working assembler before setting out to build one
    yourself. In addition, the supplied assembler provides a visual
    line-level translation GUI, and allows code comparisons with the outputs
    that your assembler will generate. For more information, see the tutorial
    in the lectures and in the submission page.
    
    Testing:
    The supplied ("built-in") Hack Assembler is guaranteed to generate
    correct binary code. This guaranteed performance can be used to test if
    another assembler, say the one written by you, also generates correct code.
    Let Prog.asm be some program written in the symbolic Hack assembly
    language. Suppose we translate this program using the supplied assembler,
    producing a binary file called Prog.hack. Next, we use another assembler
    (e.g. the one that you wrote) to translate the same program into another
    file, say MyProg.hack. Now, if the latter assembler is working correctly,
    it follows that Prog.hack == MyProg.hack. Thus, one way to test a newly
    written assembler is as follows: (i) load into the supplied visual
    assembler Prog.asm as a source program and MyProg.hack as a compare file,
    (ii) translate the source program, and (iii) compare the resulting binary
    code with the compare file (see the figure above). If the comparison
    fails, the assembler that generated MyProg.hack must be buggy; otherwise,
    it may be OK.
    """
    # Your code goes here!
    assembler: HackAssembler = HackAssembler(input_file, output_file)
    assembler.first_reading()
    assembler.second_reading()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.

    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
