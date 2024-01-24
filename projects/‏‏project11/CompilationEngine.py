"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import SymbolTable
import VMWriter
from JackTokenizer import *

CLASS_TAG = "<class>\n"
CLASS_TAG_CLOSER = "</class>\n"
CLASS_VAR_DEC_TAG = "<classVarDec>\n"
CLASS_VAR_DEC_TAG_CLOSER = "</classVarDec>\n"
SUBROUTINE_DEC_TAG = "<subroutineDec>\n"
SUBROUTINE_DEC_TAG_CLOSER = "</subroutineDec>\n"
PARAMETER_LIST_TAG = "<parameterList>\n"
PARAMETER_LIST_TAG_CLOSER = "</parameterList>\n"
SUBROUTINE_BODY_TAG = "<subroutineBody>\n"
SUBROUTINE_BODY_TAG_CLOSER = "</subroutineBody>\n"
STATEMENTS_TAG = "<statements>\n"
STATEMENTS_TAG_CLOSER = "</statements>\n"
LET_STATEMENTS_TAG = "<letStatement>\n"
LET_STATEMENTS_TAG_CLOSER = "</letStatement>\n"
WHILE_STATEMENT_TAG = "<whileStatement>\n"
WHILE_STATEMENT_TAG_CLOSER = "</whileStatement>\n"
IF_STATEMENT_TAG = "<ifStatement>\n"
IF_STATEMENT_TAG_CLOSER = "</ifStatement>\n"
RETURN_STATEMENT_TAG = "<returnStatement>\n"
RETURN_STATEMENT_TAG_CLOSER = "</returnStatement>\n"
DO_STATEMENT_TAG = "<doStatement>\n"
DO_STATEMENT_TAG_CLOSER = "</doStatement>\n"
EXPRESSION_LIST_TAG = "<expressionList>\n"
EXPRESSION_LIST_TAG_CLOSER = "</expressionList>\n"
EXPRESSION_TAG = "<expression>\n"
EXPRESSION_TAG_CLOSER = "</expression>\n"
TERM_TAG = "<term>\n"
TERM_TAG_CLOSER = "</term>\n"
VAR_DEC_TAG = "<varDec>\n"
VAR_DEC_TAG_CLOSER = "</varDec>\n"
ARGUMENT = "argument"
VAR = "var"
LABEL = "label"


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.before_dot = None
        self.while_end_counter = -1
        self.while_counter = -1
        self.current_function = None
        self.end_counter = -1
        self.if_false_counter = -1
        self.if_true_counter = -1
        self.num_expression_list = 0
        self.num_of_arguments = 0
        self.num_of_fields = 0
        self.name = None
        self.class_name = None
        self.input = input_stream
        self.tokens = input_stream.get_tokens()
        self.is_return=False
        # print(self.tokens)
        self.out = output_stream
        self.op = {'+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=',
                   '<', '>', '&'}
        self.unaryOp = {'-', '~', '^', '#'}
        self.constant = {'true', 'false', 'null', 'this'}
        self.vm_writer = VMWriter.VMWriter(self.out)
        self.table = SymbolTable.SymbolTable()
        self.function_type=None
        self.type = None
        self.kind = None
        self.function_to_call=""
        self.unary_op_dict={'~': "not", '^': "shiftleft",
                             "#": "shiftright",'-': "neg"}


        self.op_dict = {'+': "add",
                        '-': "sub",
                        '&amp;': "and",
                        '|': "or",
                        '&lt;': "lt",
                        '&gt;': "gt",
                        '=': "eq",
                        '*': "Math.multiply", '/': "Math.divide"}
        self.label_idx = 0
        self.compile_class()

    def print_advance(self):
        self.out.write(self.input.get_cur_token())
        self.input.advance()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.input.advance()  # class
        self.class_name = self.input.get_sliced_token()
        self.input.advance()#class name
        self.input.advance()  # {
        self.compile_class_var_dec()
        self.compile_subroutine()
        self.input.advance()#}

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        while self.input.get_sliced_token() in {"static", "field"}:
            self.kind = self.input.get_sliced_token()  # static or field
            # if self.kind == "field":
                # self.num_of_fields += 1
            self.input.advance()
            self.handle_type()  # int|char|boolean|className
            self.name = self.input.get_sliced_token()
            self.table.define(self.name, self.type, self.kind)
            self.input.advance()
            self.compile_comma_varName()  # ,varName
            self.input.advance()#;

    def compile_comma_varName(self):
        while self.input.get_sliced_token() == ',':
            self.input.advance()#,
            self.name = self.input.get_sliced_token()
            self.table.define(self.name, self.type,self.kind)#TODO kind local
            self.input.advance()  # varName

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        while self.input.get_sliced_token() in {"constructor", "function",
                                                "method"}:

            if self.input.get_sliced_token() == "constructor":
                self.table.start_subroutine()
                self.function_type="constructor"
                self.input.advance()  # constructor|function|method
                self.input.advance()  # void|type
                self.current_function=self.input.get_sliced_token()
                self.input.advance()  # subroutineName
                self.input.advance()  # (
                self.compile_parameter_list()
                self.input.advance()  # )
                self.subroutineBody()
            elif self.input.get_sliced_token()=="method":
                self.table.start_subroutine()
                self.function_type="method"
                self.table.define("this",self.class_name,ARGUMENT)
                self.input.advance()  # constructor|function|method
                return_val=self.input.get_sliced_token()
                self.input.advance()  # void|type
                self.current_function=self.input.get_sliced_token()#TODO
                self.input.advance()  # subroutineName
                self.input.advance()  # (
                self.compile_parameter_list()
                self.input.advance()  # )
                # self.vm_writer.write_function(self.function_to_call,
                #                               self.num_of_arguments)#TODO

                self.subroutineBody()
                # if return_val=="void":
                #     self.vm_writer.write_push("constant",0)
                #     self.vm_writer.write_return()
                    # self.vm_writer.write_pop("temp",0)
                # else:
                    # self.vm_writer.write_return()

            elif  self.input.get_sliced_token()=="function":
                self.table.start_subroutine()
                self.function_type="function"
                self.input.advance()  # function
                val_return=self.input.get_sliced_token()
                self.input.advance()  # void|type
                self.current_function=self.input.get_sliced_token()
                self.input.advance()  # subroutineName
                self.input.advance()  # (
                self.compile_parameter_list()
                self.input.advance()  # )
                self.subroutineBody()


    def subroutineBody(self):
        self.input.advance()  # {
        while self.input.get_sliced_token() == "var":
            self.compile_var_dec()
        self.vm_writer.write_function(
            self.class_name + "." + self.current_function,
            self.table.var_count("local"))
        if self.function_type=="constructor":
            self.vm_writer.write_push("constant",
                                      self.table.var_count("field"))
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("pointer", 0)
        elif self.function_type=="method":
            self.vm_writer.write_push("argument", 0)
            self.vm_writer.write_pop("pointer", 0)

        self.compile_statements()
        self.input.advance()  # }


    def type_varName(self):
        self.handle_type()
        self.name = self.input.get_sliced_token()
        self.table.define(self.name, self.type, ARGUMENT)#TODO ARGUMENT
        self.input.advance()
        while self.input.get_sliced_token() == ',':
            self.input.advance()  # ,
            self.handle_type()
            # self.input.advance()
            self.name = self.input.get_sliced_token()
            self.table.define(self.name, self.type, ARGUMENT)#TODO ARGUMENT
            self.input.advance()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        while self.input.get_sliced_token() != ")":
            self.type_varName()


    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.input.advance()  # var
        self.handle_type()  # type
        self.name = self.input.get_sliced_token()  # varName
        self.kind="local"
        self.table.define(self.name, self.type, self.kind)
        self.input.advance()
        self.compile_comma_varName()
        self.input.advance()  # ;


    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """

        while self.input.get_sliced_token() in {"let", "if"
            , "return", "do", "while"}:
            cur_token = self.input.get_sliced_token()
            if "let" == cur_token:
                self.compile_let()
            elif "if" == cur_token:
                self.compile_if()
            elif "while" == cur_token:
                self.compile_while()
            elif "do" == cur_token:
                self.compile_do()
            elif "return" == cur_token:
                self.compile_return()


    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.input.advance()  # do
        if self.table.kind_of(self.input.get_sliced_token()) == "NONE":
            self.before_dot = "NONE"
            self.function_to_call = self.input.get_sliced_token()
        else:
            self.before_dot = self.input.get_sliced_token()
            self.function_to_call = self.table.type_of(self.before_dot)
        # self.before_dot=self.input.get_sliced_token()
        # self.function_to_call=self.table.type_of(self.before_dot)
        self.input.advance()
        self.subroutine_call()
        self.input.advance()  # ;
        self.vm_writer.write_pop("temp", 0)


    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.input.advance()#let
        is_array=False
        val_to_pop_to = self.input.get_sliced_token()
        self.input.advance()#var name
        if self.input.get_sliced_token() == "[":
            is_array=True
            self.input.advance()  # [
            self.compile_expression()
            self.push(val_to_pop_to)#a[i] -> a
            self.input.advance()  # ]
            self.vm_writer.write_arithmetic("add")
        self.input.advance()  # =
        self.compile_expression()
        if is_array:
            self.vm_writer.write_pop("temp",0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp",0)
            self.vm_writer.write_pop("that",0)
        else:
            self.pop(val_to_pop_to)
        self.input.advance()  # ;


    def pop(self, val_to_pop_to):
        segment = self.table.kind_of(val_to_pop_to)
        if segment=="field":
            segment="this"
        idx = self.table.index_of(val_to_pop_to)
        self.vm_writer.write_pop(segment, idx)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.input.advance()#while
        self.input.advance()  # (
        self.while_counter+=1
        temp_while=self.while_counter
        self.vm_writer.write_label("WHILE_EXP" + self.while_counter.__str__())
        self.compile_expression()
        self.input.advance()  # )
        self.vm_writer.write_arithmetic("not")
        self.while_end_counter+=1
        temp_while_end=self.while_end_counter
        self.vm_writer.write_if("WHILE_END" + self.while_end_counter.__str__())
        self.input.advance()  # {
        self.compile_statements()
        self.input.advance()  # }
        self.vm_writer.write_goto("WHILE_EXP" + temp_while.__str__())
        self.vm_writer.write_label("WHILE_END" + temp_while_end.__str__())


    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.input.advance()#return

        if self.input.get_sliced_token() != ';':
            self.compile_expression()
        else:
            self.vm_writer.write_push("constant", 0)
        self.vm_writer.write_return()
        self.input.advance()  # ;



    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # self.if_goto_counter+=1
        # self.goto_counter+=1
        # self.end_counter+=1
        self.input.advance()  # if
        self.input.advance()  # (
        self.compile_expression()
        self.input.advance()  # )
        self.if_true_counter+=1
        self.vm_writer.write_if("IF_TRUE" + self.if_true_counter.__str__())
        self.if_false_counter+=1
        if_false=self.if_false_counter
        self.vm_writer.write_goto("IF_FALSE" + self.if_false_counter.__str__())
        self.vm_writer.write_label("IF_TRUE" + self.if_true_counter.__str__())
        self.input.advance()  # {
        self.compile_statements()
        self.input.advance()  # }
        if self.input.get_sliced_token() == "else":
            self.input.advance()  # else
            self.end_counter+=1
            if_end=self.end_counter
            self.vm_writer.write_goto("IF_END" + if_end.__str__())
            self.vm_writer.write_label("IF_FALSE" + if_false.__str__())
            self.input.advance()  # {
            self.compile_statements()
            self.input.advance()  # }
            self.vm_writer.write_label("IF_END" + if_end.__str__())
        else:
            self.vm_writer.write_label("IF_FALSE" +
            if_false.__str__())

    def subroutine_call(self):
        # counter=self.num_expression_list
        num_expression_list=0
        if self.input.get_sliced_token() == "(":
            num_expression_list += 1
            self.input.advance()  # (
            self.vm_writer.write_push("pointer",0)
            num_expression_list += self.compile_expression_list()
            self.input.advance()  # )
            self.vm_writer.write_call(
                self.class_name+"."+self.function_to_call,
                                      num_expression_list)  # TODO
        elif self.input.get_sliced_token() == ".":
            self.input.advance()  # .
            if self.table.kind_of(self.before_dot) != "NONE":
                num_expression_list+=1
                self.push(self.before_dot)
            self.function_to_call+="."+self.input.get_sliced_token()
            temp_func_name=self.function_to_call
            self.input.advance()#subroutine name

            self.input.advance()  # (
            num_expression_list += self.compile_expression_list()
            self.input.advance()  # )
            # self.vm_writer.write_call(temp_func_name,
            #                           self.num_expression_list)#TODO
            self.vm_writer.write_call(temp_func_name,
                                      num_expression_list)  # TODO
            # self.num_expression_list=counter
            # self.function_to_call=""

    def is_in_op(self) -> bool:
        toke = self.input.get_sliced_token()
        return toke in self.op

    def is_in_unaryOp(self) -> bool:
        toke = self.input.get_sliced_token()
        return toke in self.unaryOp

    def is_in_constant(self) -> bool:
        toke = self.input.get_sliced_token()
        return toke in self.constant

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()
        self.op_term()

    def op_term(self):
        while self.is_in_op():
            # self.print_advance()
            op = self.input.get_sliced_token()
            self.input.advance()
            self.compile_term()
            # op - divide to *,/ and the rest
            if op in {'*', '/'}:
                self.vm_writer.write_call(self.op_dict[op], 2)
            elif op in self.op_dict.keys():
                self.vm_writer.write_arithmetic(self.op_dict[op])

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "."
        suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """

        if self.input.token_type() == STRING_CONST:
            self.vm_writer.handle_const_str(self.input.get_sliced_token())
            self.input.advance()
        elif self.is_in_unaryOp():
            unary_op = self.input.get_sliced_token()
            self.input.advance()
            self.compile_term()
            self.vm_writer.write_arithmetic(self.unary_op_dict[unary_op])

        elif self.input.token_type() == INT_CONST:
            self.vm_writer.write_push("constant",
                                      int(self.input.get_sliced_token()))
            self.input.advance()
        elif self.input.token_type() == IDENTIFIER:
            identifier=self.input.get_sliced_token()
            self.input.advance()
            if self.input.get_sliced_token() == "[":
                self.input.advance()  # [
                self.compile_expression()
                self.push(identifier)
                self.input.advance()  # ]
                self.vm_writer.write_arithmetic("add")
                self.vm_writer.write_pop("pointer",1)
                self.vm_writer.write_push("that",0)
            elif self.input.get_sliced_token() in {".","("}:
                if self.table.kind_of(identifier)=="NONE":
                    self.before_dot="NONE"
                    self.function_to_call=identifier
                else:
                    self.before_dot=identifier
                    self.function_to_call=self.table.type_of(self.before_dot)
                self.subroutine_call()
            else:
                self.push(identifier)
        elif self.input.get_sliced_token() in self.constant:
            return_val = self.input.get_sliced_token()

            if return_val == "true":
                self.vm_writer.write_push("constant", 0)
                self.vm_writer.write_arithmetic("not")
            elif return_val == "false":
                self.vm_writer.write_push("constant", 0)
            elif return_val == "null":
                self.vm_writer.write_push("constant", 0)
            elif return_val == "this":
                self.vm_writer.write_push("pointer", 0)
            self.input.advance()
        elif self.input.get_sliced_token() == "(":
            self.input.advance()  # (
            self.compile_expression()
            self.input.advance()  # )



    def push(self, val_to_push):
        segment = self.table.kind_of(val_to_push)
        idx = self.table.index_of(val_to_push)
        if segment == "field":
            segment = "this"
        if val_to_push=="this":
            self.vm_writer.write_push("this",idx)
        self.vm_writer.write_push(segment, idx)

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        num_expression_list=0
        if self.input.get_sliced_token() != ")":
            self.compile_expression()
            num_expression_list+=1
            while self.input.get_sliced_token() == ',':
                self.input.advance()
                self.compile_expression()
                num_expression_list+=1
        return num_expression_list


    def print_advance_varName(self):
        tok = self.input.get_sliced_token()
        self.out.write(IDENTIFIER_TAG.replace(TAG, tok))
        self.input.advance()

    def print_type(self):
        if self.input.get_sliced_token().strip() in {"int", "char", "boolean"}:
            self.print_advance()
        elif self.input.token_type() == IDENTIFIER:
            self.print_advance_varName()

    def handle_type(self):
        if self.input.get_sliced_token().strip() in {"int", "char", "boolean"}:
            self.type = self.input.get_sliced_token()
            self.input.advance()
            # self.print_advance()
        elif self.input.token_type() == IDENTIFIER:
            self.type = self.input.get_sliced_token()
            self.input.advance()
            # self.print_advance_varName()
