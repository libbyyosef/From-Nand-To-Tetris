"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

ZERO="0"
ONE="1"
MINUS_ONE=-1
A="A"
D="D"
M="M"

class Code:
    """Translates Hack assembly language mnemonics into binary codes."""
    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        # Your code goes here!
        left = ZERO if mnemonic.find(A) == MINUS_ONE else ONE
        middle = ZERO if mnemonic.find(D) == MINUS_ONE else ONE
        right = ZERO if mnemonic.find(M) == MINUS_ONE else ONE
        return left + middle + right

    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        # Your code goes here!
        d_comp = {"0": "0101010", "1": "0111111", "-1": "0111010",
                  "D": "0001100", "A": "0110000",
                  "M": "1110000", "!D": "0001101", "!A": "0110001",
                  "!M": "1110001", "-D": "0001111",
                  "-A": "0110011", "-M": "1110011", "D+1": "0011111",
                  "A+1": "0110111", "M+1": "1110111",
                  "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
                  "D+A": "0000010", "D+M": "1000010",
                  "D-A": "0010011", "D-M": "1010011", "A-D": "0000111",
                  "M-D": "1000111", "D&A": "0000000",
                  "D&M": "1000000", "D|A": "0010101", "D|M": "1010101",
                  "A<<":"0100000", "D<<":"0110000", "M<<":"1100000",
                  "A>>":"0000000","D>>":"0010000","M>>":"1000000"}
        return d_comp[mnemonic]

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        # Your code goes here!
        d_jump = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
                  'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}
        return d_jump[mnemonic]
