"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

KEYWORD = "KEYWORD"
SYMBOL = "SYMBOL"
IDENTIFIER = "IDENTIFIER"
INT_CONST = "INT_CONST"
STRING_CONST = "STRING_CONST"

TAG = "tag"

KEYWORD_TAG = "<keyword> tag </keyword>\n"
IDENTIFIER_TAG = "<identifier> tag </identifier>\n"

SYMBOL_TAG = "<symbol> tag </symbol>\n"
INT_CONST_TAG = "<integerConstant> tag </integerConstant>\n"
STR_CONST_TAG = "<stringConstant> tag </stringConstant>\n"


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' |
               'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of
    tokens
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_stream.read().splitlines()

        self.__word_identifier = ""
        self.__input_file = input_stream.read()
        self.input_str_no_commas = ""
        self.parse_remove_commas()
        # print(self.input_str_no_commas)
        self.__input_lines = self.input_str_no_commas.split(" ")
        self.__words = []
        self.__str_dict = {}
        self.read_file_and_parse()
        self.__current_line = ""
        self.statements={'let': KEYWORD,
                                    'do': KEYWORD,
                                    'if': KEYWORD,
                                    'while': KEYWORD,
                                    'return': KEYWORD}
        self.__integerConstant = list(range(32767))
        self.__dict_tokens_types = {'class': KEYWORD, 'constructor': KEYWORD,
                                    'function': KEYWORD, 'method': KEYWORD,
                                    'field': KEYWORD,
                                    'static': KEYWORD, 'var': KEYWORD,
                                    'int': KEYWORD,
                                    'char': KEYWORD, 'boolean': KEYWORD,
                                    'void': KEYWORD,
                                    'true': KEYWORD, 'false': KEYWORD,
                                    'null': KEYWORD,
                                    'this': KEYWORD, 'let': KEYWORD,
                                    'do': KEYWORD,
                                    'if': KEYWORD,
                                    'else': KEYWORD, 'while': KEYWORD,
                                    'return': KEYWORD,
                                    '{': SYMBOL, '}': SYMBOL, '(': SYMBOL,
                                    ')': SYMBOL, '[': SYMBOL,
                                    ']': SYMBOL,
                                    '.': SYMBOL, ',': SYMBOL,
                                    ';': SYMBOL, '+': SYMBOL,
                                    '-': SYMBOL, '*': SYMBOL, '/': SYMBOL,
                                    '&': SYMBOL, '|': SYMBOL,
                                    '<': SYMBOL,
                                    '>': SYMBOL, '=': SYMBOL,
                                    '~': SYMBOL, '^': SYMBOL, '#': SYMBOL
                                    }


        self.__extend_dict_type = self.__dict_tokens_types.copy()
        for i in self.__integerConstant:
            self.__extend_dict_type[str(i)] = INT_CONST
        self.__tokens_array = []
        self.__token_type = None
        self.__token_idx = 0
        self.token_parsing()
        for s in self.__str_dict:
            self.__extend_dict_type[s] = STRING_CONST
        # print(self.__tokens_array)
        # print(self.__str_dict)
        self.__current_token = self.__tokens_array[self.__token_idx]


    def read_file_and_parse(self):
            words_split = self.input_str_no_commas.split(" ")
            # Iterate through the words
            # print(words_split)
            i = 0
            while i < len(words_split):
                if words_split[i].__contains__('"'):
                    phrase = []
                    phrase.append(words_split[i])
                    i += 1
                    if phrase[0].count('"')==1:
                        while i < len(words_split) and not \
                                words_split[
                            i].__contains__(
                            '"'):
                            phrase.append(words_split[i])
                            i += 1
                        if i < len(words_split):
                            phrase.append(words_split[i])
                    tmp=self.handle_commas(" ".join(phrase))
                    if tmp!="":
                        # words_split[i]=tmp
                        self.__words.append(tmp)
                else:
                    self.__words.append(words_split[i])
                i += 1

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        return self.__token_idx != len(self.__tokens_array) - 1

        # ???

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true.
        Initially there is no current token.
        """
        # Your code goes here!
        if self.has_more_tokens():
            self.__token_idx += 1
            self.__current_token = self.__tokens_array[self.__token_idx]

    def token_parsing(self):

        for word in self.__words:
            if len(word)!=0:
                # print(word)
                self.convert_word_token(word)

    def convert_word_token(self, word):
        if word in self.__dict_tokens_types:
            self.__tokens_array.append(self.format_word(word))
        elif word in self.__str_dict:
            self.__tokens_array.append(STR_CONST_TAG.replace(TAG, word))
        else:
            self.handle_single_word(word)

    def format_word(self, word):
        if self.__extend_dict_type[word] == KEYWORD:
            return KEYWORD_TAG.replace(TAG, word)
        elif self.__extend_dict_type[word] == SYMBOL:
            if word == "<":
                return SYMBOL_TAG.replace(TAG, "&lt;")
            elif word == ">":
                return SYMBOL_TAG.replace(TAG, "&gt;")
            elif word == "&":
                return SYMBOL_TAG.replace(TAG, "&amp;")
            else:
                return SYMBOL_TAG.replace(TAG, word)

    def handle_single_word(self, word):
        i = 0
        while i < len(word):
            current_letter = word[i]
            if current_letter in self.__dict_tokens_types:
                if self.__word_identifier.strip()=="":

                    self.__word_identifier=""


                if self.__word_identifier != "" and \
                        self.__dict_tokens_types[current_letter] == SYMBOL:
                    if self.__word_identifier in \
                            self.__dict_tokens_types:
                        self.__tokens_array.append(
                            self.format_word(self.__word_identifier))
                        self.__word_identifier = ""
                    elif self.__word_identifier.isnumeric() and \
                            int(self.__word_identifier) in \
                            self.__integerConstant:
                        self.__tokens_array.append(
                            INT_CONST_TAG.replace(TAG,
                                                  self.__word_identifier))
                        self.__word_identifier = ""
                    else:
                        self.__tokens_array.append(
                            IDENTIFIER_TAG.replace(TAG,
                                                   self.__word_identifier))
                        self.__extend_dict_type[
                            self.__word_identifier] = IDENTIFIER
                        self.__word_identifier = ""
                self.__tokens_array.append(
                    self.format_word(current_letter))

            else:
                if self.__current_line==" ":
                    if self.__word_identifier != "":

                        if self.__word_identifier in self.__dict_tokens_types:
                            self.__tokens_array.append(self.format_word(
                                self.__word_identifier))
                            self.__word_identifier = ""
                        elif self.__word_identifier.isnumeric() and \
                                int(self.__word_identifier) in \
                                self.__integerConstant:
                            self.__tokens_array.append(
                                INT_CONST_TAG.replace(TAG,
                                                      self.__word_identifier))
                            self.__word_identifier = ""
                        else:
                            if self.__word_identifier.strip() != "":
                                self.__tokens_array.append(
                                    IDENTIFIER_TAG.replace(TAG,
                                                           self.__word_identifier.strip()))
                                self.__extend_dict_type[
                                    self.__word_identifier.strip()] = IDENTIFIER
                                self.__word_identifier = ""
                if self.__word_identifier.strip() == "":
                    self.__word_identifier = ""
                self.__word_identifier += current_letter

            i += 1
        if self.__word_identifier != "":

            if self.__word_identifier in self.__dict_tokens_types:
                self.__tokens_array.append(self.format_word(
                    self.__word_identifier))
                self.__word_identifier = ""
            elif self.__word_identifier.isnumeric() and \
                    int(self.__word_identifier) in \
                    self.__integerConstant:
                self.__tokens_array.append(
                    INT_CONST_TAG.replace(TAG, self.__word_identifier))
                self.__word_identifier = ""
            else:
                if self.__word_identifier.strip()!="":
                    self.__tokens_array.append(
                        IDENTIFIER_TAG.replace(TAG, self.__word_identifier.strip()))
                    self.__extend_dict_type[self.__word_identifier.strip()] = IDENTIFIER
                    self.__word_identifier = ""

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        # Your code goes here!

        return self.__extend_dict_type[self.get_sliced_token()]

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        return self.__current_token.upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' |
            '+' |
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        # Your code goes here!
        return self.__current_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_')
            not
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!
        return self.__current_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        # Your code goes here!
        return int(self.__current_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Your code goes here!
        return self.__current_token

    def handle_commas(self, sentence):
        before = sentence.find('"')
        after = sentence.find('"', before + 1)
        before_str = sentence[:before]
        middle_str = sentence[before+1:after]
        after_str = sentence[after + 1:]
        self.__words.append(before_str)
        self.__words.append(middle_str)

        self.__str_dict[middle_str] = STRING_CONST
        return after_str

    def get_tokens(self):
        return self.__tokens_array

    def get_dict_tokens(self):
        return self.__extend_dict_type

    def get_cur_token(self):
        return self.__current_token

    def get_sliced_token(self):
        start = self.__current_token.find('>')
        end = self.__current_token.find("<", start + 1)
        temp_token = self.__current_token[start + 1:end]
        if "<stringConstant>" not in self.__current_token:
            temp_token=temp_token.strip()
        else:
            temp_token=temp_token[:-1].lstrip()
        return temp_token

    def get_str_dict(self):
        return self.__str_dict

    def parse_remove_commas(self):
        i = 0
        while i < len(self.__input_file):
            if self.__input_file[i] in {"\n", "\t"}:
                self.input_str_no_commas+=" "
                i+=1
            elif self.__input_file[i]=='"':
                self.input_str_no_commas += self.__input_file[i]
                i+=1
                while i<len(self.__input_file) :
                    if self.__input_file[i]!='"':
                        self.input_str_no_commas += self.__input_file[i]
                        i += 1
                    if self.__input_file[i]=='"':
                        self.input_str_no_commas += self.__input_file[i]
                        i+=1
                        break
                # self.input_str_no_commas += self.__input_file[i]
            elif self.__input_file[i]=='/' and i+1<len(self.__input_file):
                if self.__input_file[i+1]=='*':
                    i+=2
                    while i+1< len(self.__input_file) :
                        if self.__input_file[i]=='*' and self.__input_file[
                            i+1]=='/':
                            i+=2
                            break
                        i+=1
                elif self.__input_file[i+1]=='/':
                    i+=2
                    while i< len(self.__input_file) :
                        if self.__input_file[i]!='\n':
                            i+=1
                        else:
                            break
                else:
                    self.input_str_no_commas+='/'
                    i+=1
            else:
                self.input_str_no_commas+=self.__input_file[i]
                i+=1

