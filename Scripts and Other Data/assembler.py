# Assembler terminal output should be in this format:
# |----Instruction----|    |--------Data-------|
# |  8  37  38  39   5|    |  0   0   0   0   0|
# |  6   7   7  72  51|    |  0   0   0   0   0|
# |  7  72  50  37 136|    |  1   0   0   5   0|
# | 51  37 136  38  37|    |  0   7   0   1   4|
# |136  51  38  37 136|    |  0   0   1   3   0|
# | 51  38  37 136 208|    |  0  20   2   0   0|
# |  0   0            |    |  0   0            |

# It can also be in this format:
# 0x08 0x26 0x27 0x28 0x05 ... <end of instructions> 0xFF
# 0x00 0x00 0x00 0x00 0x00 ... <end of data> 0xFE

# Assembly instructions:
# NOP         - Instruc[x00]                                            # This is the NOP instruction
# STR <data> <addr> - Instruc[x05 x06 x07] Data[x04 <data> <addr>]      # This stores data to an address in RAM
# ZOR         - Instruc[x08 | x18]                                      # These clear the output register
# STRA <data> - Instruc[x25 : x27] Data[<data>]                         # This stores data to the ALU registers
# PASS <A>    - Instruc[x25 x27]     Data[x00 <A>]                      # Pass a byte through ALU

# if an argument is a RAM address, it needs to be prefixed with 'a' (e.g., a0, a1, a2, etc.)
# furthermore, the assembler needs to get and load the proper address from RAM:
# the bytecode for that is: Instruc[x05 x07 x48] Data[x01 <addr> x00]
# The bytecode above will load the value at the ram address into the output register

# The assembler will then need to store the value in the correct register, depending on the instruction
# Any of the alu instructions that take two arguments will need to load the first argument into r3
# and the second argument into r2
# So the value in the output register will need to be stored in r3 or r2
# For the RAM instructions, the assembler will need to load the address into r7 or r6

# If both arguments are RAM addresses, the assembler will need to load the first address into r7
# and the second address into r6, using the method detailed above.

# SUB <A> <B> - Instruc[x25 x26 x27] Data[x01 <A> <B>]                  # Subtract B from A
# ADD <A> <B> - Instruc[x25 x26 x27] Data[x02 <A> <B>]                  # Add A and B
# MUL <A> <B> - Instruc[x25 x26 x27] Data[x03 <A> <B>]                  # Multiply A and B
# AND <A> <B> - Instruc[x25 x26 x27] Data[x04 <A> <B>]                  # AND A and B
# XOR <A> <B> - Instruc[x25 x26 x27] Data[x05 <A> <B>]                  # XOR A and B
# OR  <A> <B> - Instruc[x25 x26 x27] Data[x06 <A> <B>]                  # OR A and B
# NOT <A>     - Instruc[x25 x27]     Data[x07 <A>]                      # NOT A
# SOR <r5 : r7 | r1 : r3>   - Instruc[x15 : x17 | x35 : x37]            # This stores the output register to a writable register
# SMO         - Instruc[x48]                                            # Read RAM output to the output register
# SAO         - Instruc[x88]                                            # Read ALU output to the output register
# JMP <addr>  - Instruc[xC0] Data[<addr>]                               # Jump to a hardcoded instruction address
# JMP r0      - Instruc[xD0]                                            # Jump to the instruction address stored in r0

# Registers that are passed as arguments are written like this: r<register number>
# RAM addresses are passed as arguments like this: a<address>

# these are an invalid instructions, throw an error if they are found when validating ROM files or assembling
# INVALID     - Instruc[x01 : x04]
# INVALID     - Instruc[x09 : x0F]
# INVALID     - Instruc[x10 : x14]
# INVALID     - Instruc[x19 : x1F]
# INVALID     - Instruc[x20 : x24]
# INVALID     - Instruc[x28 : x2F]
# INVALID     - Instruc[x30 : x34]
# INVALID     - Instruc[x38 : x47]
# INVALID     - Instruc[x49 : x87]
# INVALID     - Instruc[x89 : xBF]
# INVALID     - Instruc[xC1 : xCF]
# INVALID     - Instruc[xD1 : xFD]

# The assembler will have several different flags:
# The -f flag will take a file as an argument and assemble it
# The -v flag will take a file as an argument and validate it
# The -h flag that will print the help message
# The -o flag that will take a file as an argument and output the assembled file to that file
# The -d flag that will take a file as an argument and output the assembled file to that file in a human readable format

# The assembler can also take in direct input from the user if no flags are specified