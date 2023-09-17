// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.

	@R14 //initialization
	D=M
	@addmax
	M=D
	@R14
	D=M
	@addmin
	M=D
	@R14
	A=M
	D=M
	@max
	M=D
	@min
	M=D
	@i
	M=0 //
	@LOOP
	0;JMP

(LOOP)
	@R15
	D=M
	@i
	D=D-M
	@SWP //out of loop
	D;JLE
	@R14
	D=M
	@i
	D=D+M
	A=D
	D=M
	@min
	D=D-M
	@MINUPDATE
	D;JLT
	@R14
	D=M
	@i
	D=D+M
	A=D
	D=M
	@max
	D=D-M
	@MAXUPDATE
	D;JGT
	@i
	M=M+1
	@LOOP
	0;JMP

(MINUPDATE)
	@R14
	D=M
	@i
	D=D+M
	A=D
	D=M
	@min
	M=D
	@R14
	D=M
	@i
	D=D+M
	@addmin
	M=D
	@i
	M=M+1
	@LOOP
	0;JMP

(MAXUPDATE)
	@R14
	D=M
	@i
	D=D+M
	A=D
	D=M
	@max
	M=D
	@R14
	D=M
	@i
	D=D+M
	@addmax
	M=D
	@i
	M=M+1
	@LOOP
	0;JMP

(SWP)
	@max
	D=M
	@addmin
	A=M
	M=D

	@min
	D=M
	@addmax
	A=M
	M=D

	@END
	0;JMP





(END)
	@END
	0;JMP
