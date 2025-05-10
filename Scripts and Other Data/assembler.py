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
# x08 x26 x27 x28 x05 ... <end of instructions> xFF x01
# x00 x00 x00 x00 x00 ... <end of data> xFF x02

# Assembly instructions:
# NOP         - Instruc[x00 : x04]                                 # these are a NOP instructions
# STR <data> <addr> - Instruc[x05 x06 x07] Data[x04 <data> <addr>] # this stores data to an address in RAM
# ZOR         - Instruc[x08]                                       # this clears the output register
# INVALID     - Instruc[x09 : x0F]                                 # these are an invalid instructions, throw an error if they are found when validating ROM files or assembling
# NOP         - Instruc[x10 : x14]                                 # these read from the output register but doesn't store it anywhere, effectively a NOP
# LOR <data>  - Instruc[x15 : x17 | x25 : x27] Data[<data>]        # this loads a literal into a writable register (r1 : r3 | r5 : r7)
# ZOR         - Instruc[x18]                                       # this clears the output register
# INVALID     - Instruc[x19 : x1F]                                 # these are an invalid instructions, throw an error if they are found when validating ROM files or assembling
# NOP         - Instruc[x20 : x24]                                 # these instructions sets high the ALU select lines, but don't store anything, effectively a NOP
# STRA <data> - Instruc[x25 : x27] Data[<data>]                    # this stores data to the ALU registers
# PASS <A>    - Instruc[x25 x27]     Data[x00 <A>]                 # pass a byte through ALU
# SUB <A> <B> - Instruc[x25 x26 x27] Data[x01 <A> <B>]             # subtract B from A
# ADD <A> <B> - Instruc[x25 x26 x27] Data[x02 <A> <B>]             # add A and B
# MUL <A> <B> - Instruc[x25 x26 x27] Data[x03 <A> <B>]             # multiply A and B
# AND <A> <B> - Instruc[x25 x26 x27] Data[x04 <A> <B>]             # AND A and B
# XOR <A> <B> - Instruc[x25 x26 x27] Data[x05 <A> <B>]             # XOR A and B
# OR  <A> <B> - Instruc[x25 x26 x27] Data[x06 <A> <B>]             # OR A and B
# NOT <A>     - Instruc[x25 x27]     Data[x07 <A>]                 # NOT A
# INVALID     - Instruc[x28 : x2F]                                 # these are an invalid instructions, throw an error if they are found when validating ROM files or assembling
# NOP         - Instruc[x30 : x34]                                 # these instructions read the output register to the ALU, but don't store anything, effectively a NOP
# SOR <r1 : r3>   - Instruc[x35 : x37]                             # this stores the output register to an ALU register