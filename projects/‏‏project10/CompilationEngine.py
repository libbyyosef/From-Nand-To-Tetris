"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

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
        self.input = input_stream
        self.tokens = input_stream.get_tokens()
        # print(self.tokens)
        self.out = output_stream
        self.op = {'+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=',
                   '<','>','&'}
        self.unaryOp = {'-', '~', '^', '#'}
        self.constant = {'true', 'false', 'null', 'this'}

        self.compile_class()

    def print_advance(self):
        self.out.write(self.input.get_cur_token())
        self.input.advance()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.out.write(CLASS_TAG)
        self.print_advance()  # class
        self.print_advance_varName()  # className
        self.print_advance()  # {
        self.compile_class_var_dec()
        self.compile_subroutine()
        self.print_advance()  # }
        self.out.write(CLASS_TAG_CLOSER)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!

        while self.input.get_sliced_token() in {"static", "field"}:
            self.out.write(CLASS_VAR_DEC_TAG)
            self.print_advance()
            self.print_type()  # int|char|boolean|className
            self.print_advance_varName()  # varName
            self.compile_comma_varName()  # ,varName
            self.print_advance()  # ;
            self.out.write(CLASS_VAR_DEC_TAG_CLOSER)

    def compile_comma_varName(self):
        while self.input.get_sliced_token() == ',':
            self.print_advance()  # ,
            self.print_advance_varName()  # varName

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!

        while self.input.get_sliced_token() in {"constructor", "function",
                                                "method"}:
            self.out.write(SUBROUTINE_DEC_TAG)
            self.print_advance()  # constructor|function|method
            self.print_advance()  # void|type
            self.print_advance_varName()  # subroutineName
            self.print_advance()  # (
            self.compile_parameter_list()
            self.print_advance()  # )
            self.subroutineBody()
            self.out.write(SUBROUTINE_DEC_TAG_CLOSER)

    def subroutineBody(self):
        self.out.write(SUBROUTINE_BODY_TAG)
        self.print_advance()  # {
        while self.input.get_sliced_token() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.print_advance()  # }
        self.out.write(SUBROUTINE_BODY_TAG_CLOSER)

    def type_varName(self):
        self.print_type()
        self.print_advance_varName()
        while self.input.get_sliced_token() ==',':
            self.print_advance()
            self.print_type()
            self.print_advance_varName()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.out.write(PARAMETER_LIST_TAG)
        while self.input.get_sliced_token() != ")":
            self.type_varName()
        self.out.write(PARAMETER_LIST_TAG_CLOSER)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.out.write(VAR_DEC_TAG)
        self.print_advance()  # var
        self.print_type()  # type
        self.print_advance_varName()  # varName
        self.compile_comma_varName()
        self.print_advance()#;
        self.out.write(VAR_DEC_TAG_CLOSER)

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        self.out.write(STATEMENTS_TAG)
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
        self.out.write(STATEMENTS_TAG_CLOSER)

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.out.write(DO_STATEMENT_TAG)
        self.print_advance()  # do
        self.print_advance_varName()
        self.subroutine_call()
        self.print_advance()  # ;
        self.out.write(DO_STATEMENT_TAG_CLOSER)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.out.write(LET_STATEMENTS_TAG)
        self.print_advance()
        self.print_advance_varName()  # varName
        if self.input.get_sliced_token() == "[":
            self.print_advance()  # [
            self.compile_expression()
            self.print_advance()  # ]
        self.print_advance()  # =
        self.compile_expression()
        self.print_advance()  # ;
        self.out.write(LET_STATEMENTS_TAG_CLOSER)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.out.write(WHILE_STATEMENT_TAG)
        self.print_advance()
        self.print_advance()  # (
        self.compile_expression()
        self.print_advance()  # )
        self.print_advance()  # {
        self.compile_statements()
        self.print_advance()  # }
        self.out.write(WHILE_STATEMENT_TAG_CLOSER)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.out.write(RETURN_STATEMENT_TAG)
        self.print_advance()
        if self.input.get_sliced_token() != ';':
            self.compile_expression()
        self.print_advance()  # ';
        self.out.write(RETURN_STATEMENT_TAG_CLOSER)

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.out.write(IF_STATEMENT_TAG)
        self.print_advance()  # if
        self.print_advance()  # (
        self.compile_expression()
        self.print_advance()  # )
        self.print_advance()  # {
        self.compile_statements()
        self.print_advance()  # }
        if self.input.get_sliced_token() == "else":
            self.print_advance()  # else
            self.print_advance()  # {
            self.compile_statements()
            self.print_advance()  # }
        self.out.write(IF_STATEMENT_TAG_CLOSER)

    def subroutine_call(self):
        if self.input.get_sliced_token() == "(":
            self.print_advance()  # (
            self.compile_expression_list()
            self.print_advance()  # )
        elif self.input.get_sliced_token() == ".":
            self.print_advance()  # .
            self.print_advance_varName()  # subroutineName
            self.print_advance()  # (
            self.compile_expression_list()
            self.print_advance()  # )

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
        # Your code goes here!
        self.out.write(EXPRESSION_TAG)
        self.compile_term()
        self.op_term()
        self.out.write(EXPRESSION_TAG_CLOSER)

    def op_term(self):
        while self.is_in_op():
            self.print_advance()
            self.compile_term()

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
        self.out.write(TERM_TAG)
        if self.input.get_sliced_token() in self.constant:
            self.print_advance()
        elif self.input.token_type() == STRING_CONST:
            self.print_advance()
        elif self.is_in_unaryOp():
            self.print_advance()
            self.compile_term()
        elif self.input.token_type() == INT_CONST:
            self.print_advance()
        elif self.input.token_type() == IDENTIFIER:

            self.print_advance()
            if self.input.get_sliced_token() == "[":
                self.print_advance()  # [
                self.compile_expression()
                self.print_advance()  # ]
            else:
                self.subroutine_call()
        elif self.input.get_sliced_token() == "(":
            self.print_advance()  # (
            self.compile_expression()
            self.print_advance()  # )

        self.out.write(TERM_TAG_CLOSER)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""

        self.out.write(EXPRESSION_LIST_TAG)
        if self.input.get_sliced_token() != ")":
            self.compile_expression()
            while self.input.get_sliced_token() == ',':
                self.print_advance()
                self.compile_expression()

        self.out.write(EXPRESSION_LIST_TAG_CLOSER)

    def print_advance_varName(self):
        tok = self.input.get_sliced_token()
        self.out.write(IDENTIFIER_TAG.replace(TAG, tok))

        self.input.advance()

    def print_type(self):
        if self.input.get_sliced_token().strip() in {"int", "char", "boolean"}:
            self.print_advance()
        elif self.input.token_type() == IDENTIFIER:
            self.print_advance_varName()

