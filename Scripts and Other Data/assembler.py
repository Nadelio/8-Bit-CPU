# Assembler output should be in this format:
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
# LRG <register> <data>  - Instruc[x15 : x17 | x25 : x27] Data[<data>]  # This loads a literal into a writable register (r1 : r3 | r5 : r7)
# STRA <data> - Instruc[x25 : x27] Data[<data>]                         # This stores data to the ALU registers
# PASS <A>    - Instruc[x25 x27]     Data[x00 <A>]                      # Pass a byte through ALU
# SUB <A> <B> - Instruc[x25 x26 x27] Data[x01 <A> <B>]                  # Subtract B from A
# ADD <A> <B> - Instruc[x25 x26 x27] Data[x02 <A> <B>]                  # Add A and B
# MUL <A> <B> - Instruc[x25 x26 x27] Data[x03 <A> <B>]                  # Multiply A and B
# AND <A> <B> - Instruc[x25 x26 x27] Data[x04 <A> <B>]                  # AND A and B
# XOR <A> <B> - Instruc[x25 x26 x27] Data[x05 <A> <B>]                  # XOR A and B
# OR  <A> <B> - Instruc[x25 x26 x27] Data[x06 <A> <B>]                  # OR A and B
# NOT <A>     - Instruc[x25 x27]     Data[x07 <A>]                      # NOT A
# SOR <r1 : r3>   - Instruc[x35 : x37]                                  # This stores the output register to an ALU register
# SMO         - Instruc[x48]                                            # Read RAM output to the output register
# SAO         - Instruc[x88]                                            # Read ALU output to the output register
# JMP <addr>  - Instruc[xC0] Data[<addr>]                               # Jump to an address in RAM
# JMP r0      - Instruc[xD0]                                            # Jump to the address in r0

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