"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP="C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"


parser_num=0


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO,
        bootstrap: bool) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        bootstrap (bool): if this is True, the current file is the 
            first file we are translating.
    """
    # Your code goes here!
    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)
    global_function_name = code_writer.get_file_name()
    global_function_name = global_function_name.split("\\")[-1]
    #global_function_name = global_function_name[:global_function_name.find(
    # ".")]
    code_writer.set_file_name(global_function_name)
    # print(global_function_name)
    # code_writer.set_file_name(name)
    if bootstrap:
        code_writer.write_init()
    parser.init_update_args_cmt_type()
    while parser.has_more_commands():

        if parser.command_type() == C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1())

        elif parser.command_type() == C_PUSH:
            if parser.memory_place()=="static":
                name = input_file.name
                file = name.split("\\")
                filename = file[-1]
                #name = name[:name.find(".")]
                code_writer.set_file_name(filename)

            code_writer.write_push_pop(parser.arg1(), parser.memory_place(),
                                       parser.arg2())
            code_writer.set_file_name(global_function_name)


        elif parser.command_type() == C_POP:
            if parser.memory_place()=="static":
                name = input_file.name
                file = name.split("\\")
                file1 = file[-1]
                #name = name[:name.find(".")]
                code_writer.set_file_name(file1)
            code_writer.write_push_pop(parser.arg1(), parser.memory_place(),
                                       parser.arg2())
            code_writer.set_file_name(global_function_name)
        elif parser.command_type()==C_LABEL:
            code_writer.write_label(parser.arg0())
        elif parser.command_type()==C_GOTO:
            code_writer.write_goto(parser.arg0())
        elif parser.command_type()==C_IF:
            code_writer.write_if(parser.arg0())
        elif parser.command_type() ==C_FUNCTION:
            code_writer.write_function(parser.arg0(),parser.arg2())
        elif parser.command_type()==C_CALL:
            code_writer.write_call(parser.arg0(),parser.arg2())
        elif parser.command_type()==C_RETURN:
            code_writer.write_return()
        code_writer.next_line()
        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                # parser_num= len(files_to_translate)
                translate_file(input_file, output_file, bootstrap)
            bootstrap = False
