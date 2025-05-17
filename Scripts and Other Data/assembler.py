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
# ZOR         - Instruc[x08 | x18]                                      # These clear the output register
# STRM <data> <addr> - Instruc[x05 x06 x07] Data[x04 <data> <addr>]     # This stores data to an address in RAM
# STRA <register> <data> - Instruc[x25 : x27] Data[<data>]              # This stores data to the ALU registers

# if an argument is a RAM address, it needs to be prefixed with 'a' (e.g., a0, a1, a2, etc.)
# furthermore, the assembler needs to get and load the proper address from RAM:
# the bytecode for that is: Instruc[x05 x07 x48] Data[x01 <addr> x00]
# The bytecode above will load the value at the ram address into the output register

# The assembler will then need to store the value in the correct register, depending on the instruction
# Any of the alu instructions that take two arguments will need to load the first argument into r3
# and the second argument into r2
# So the value in the output register will need to be stored in r3 or r2

# If both arguments are RAM addresses, the assembler will need to load the first address into r7
# and the second address into r6, using the method detailed above.

# PASS <A>    - Instruc[x25 x27]     Data[x00 <A>]                      # Pass a byte through ALU
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

import re
from enum import Enum

class Colors(Enum):
    COMPILER_FATAL = "\033[35m" # purple
    FATAL = "\033[91m"   # red
    SUCCESS = "\033[92m" # green
    WARNING = "\033[93m" # yellow
    INFO = "\033[94m"    # blue
    MESSAGE = "\033[96m" # cyan
    RESET = "\033[0m"

class Instruction:
    instructions = [[]]
    data = []
    argc = 0

    def __init__(self, instructions, data, argc=0):
        self.instructions = instructions
        self.data = data
        self.argc = argc

    def __str__(self):
        return f"{Colors.MESSAGE}Instruction Bytes: {Colors.INFO}{self.instructions}{Colors.MESSAGE},\nData Bytes:        {Colors.INFO}{self.data}{Colors.RESET}"


instruction_map = {
    "nop" : Instruction([0x00], [0x00]),
    "zor" : Instruction([[0x08], [0x18]], [0x0]),
    "strm" : Instruction([0x05, 0x06, 0x07], [0x04], 2),
    "stra" : Instruction([[0x25], [0x26], [0x27]], [], 1),
    "pass" : Instruction([0x25, 0x27], [0x00], 1),
    "sub" : Instruction([0x25, 0x26, 0x27], [0x01], 2),
    "add" : Instruction([0x25, 0x26, 0x27], [0x02], 2),
    "mul" : Instruction([0x25, 0x26, 0x27], [0x03], 2),
    "and" : Instruction([0x25, 0x26, 0x27], [0x04], 2),
    "xor" : Instruction([0x25, 0x26, 0x27], [0x05], 2),
    "or"  : Instruction([0x25, 0x26, 0x27], [0x06], 2),
    "not" : Instruction([0x25, 0x27], [0x07], 1),
    "sor" : Instruction([[0x15], [0x16], [0x17], [0x35], [0x36], [0x37]], [], 1),
    "smo" : Instruction([0x48], [], 0),
    "sao" : Instruction([0x88], [], 0),
    "jmp" : Instruction([0xC0], [], 1),
    "jmp_r0" : Instruction([0xD0], [], 0),
}

alu_instructions = [
    "pass",
    "sub",
    "add",
    "mul",
    "and",
    "xor",
    "or",
    "not",
]

class Assembler:

    input = ""
    instructions, data = []
    current_line = 0

    def __init__(self, input):
        self.input = input
        self.instructions = []
        self.data = []

    def assemble(self):
        """
        Currently unimplemented.
        Assemble the input and return the assembled bytecode.
        """

        for line in self.input.splitlines():
            self.parse_instruction(line)
            self.current_line += 1
        
        self.validate()
        # return self.format()
        raise NotImplementedError(f"{Colors.COMPILER_FATAL}Assemble method is not implemented yet.{Colors.RESET}")
    
    def validate_file(file):
        """
        Validate an existing file.
        """
        raise NotImplementedError(f"{Colors.COMPILER_FATAL}Validate file method is not implemented yet.{Colors.RESET}")

    def format(self):
        """
        Format the output of the assembler.
        """
        raise NotImplementedError(f"{Colors.COMPILER_FATAL}Format method is not implemented yet.{Colors.RESET}")
    
    def deformat(input, json=False):
        """
        Deformat the bytecode into a raw byte sequence, or a json object containing two arrays.
        """

        # if json:
        #     # Convert the input to a JSON object
        #     return {
        #         "instructions": [...],
        #         "data": [...]
        #     }

        raise NotImplementedError(f"{Colors.COMPILER_FATAL}Deformat method is not implemented yet.{Colors.RESET}")

    def __validate(self):
        """
        Validate the output of the assembler. Called by the assembler directly
        """
        raise NotImplementedError(f"{Colors.COMPILER_FATAL}Validate method is not implemented yet.{Colors.RESET}")

    def process_address(self, address, index, instruction):
        """
        Process a RAM address and return the corresponding bytecode.
        """

        # Check if the address is valid
        if not address[1:].isdigit() or int(address[1:]) < 0 or int(address[1:]) > 255:
            raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid RAM address:\n\t\t{address}")

        # Check if the instruction is valid
        if instruction not in alu_instructions:
            raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid instruction with address argument:\n\t\t{instruction}")

        if index == 0:
            # If the address is the first argument, load it into r7
            return [0x05, 0x07, 0x48, 0x37], [0x01, int(address[1:]), 0x00, 0x00], 0
        elif index == 1:
            # If the address is the second argument, load it into r6
            return [0x05, 0x06, 0x48, 0x36], [0x01, int(address[1:]), 0x00, 0x00], 1
        else:
            raise ValueError(f"{Colors.COMPILER_FATAL}Compiler Error on line: {Colors.INFO}{self.current_line}{Colors.COMPILER_FATAL}.\n\tInvalid index for address argument:\n\t\t{Colors.INFO}{index}{Colors.RESET}")

    def process_instruction(self, instruction, arg_states, args, arg_metadata):
        """
        Process an instruction and return the corresponding bytecode.
        """
        
        # Check if the instruction is valid
        if instruction not in instruction_map:
            raise ValueError(f"{Colors.FATAL}Error on line: {Colors.INFO}{self.current_line}{Colors.FATAL}.\n\tInvalid instruction:\n\t\t{Colors.INFO}{instruction}{Colors.RESET}")
        
        # need to utilize the arg_states and args to get the correct instruction bytes
        # to prevent extraneous bytes from being added to the instruction, use the arg_metadata list

        # for ALU instructions, the metadata will be the index of the address arguments (if they exist), remove the x26 and/or x27 instructions if they exist 


        raise NotImplementedError(f"{Colors.COMPILER_FATAL}Process instruction method is not implemented yet.{Colors.RESET}")

    def parse_instruction(self, instruction):
        """
        Parse an instruction and return the corresponding bytecode.
        """
        # Remove comments and extra whitespace
        instruction = re.sub(r'\s+', ' ', instruction)
        instruction = instruction.split(";")[0].strip()

        # Split the instruction into parts
        parts = instruction.split()
        # Get the instruction name
        instr_name = parts[0].lower()
        # Get the arguments
        args = parts[1:]
        
        # Check if the instruction is valid
        if instr_name not in instruction_map:
            raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid instruction:\n\t\t{instr_name}")
        
        # Get the instruction object
        instr_obj = instruction_map[instr_name]
        
        # Check if the number of arguments is correct
        if len(args) != instr_obj.argc:
            raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid number of arguments for {instr_name}:\n\t\texpected {instr_obj.argc}, got {len(args)}")
        
        later = []

        arg_states = []
        # Check if the arguments are registers, RAM addresses, or immediate values
        if len(args) > 0:
            for arg in args:
                if arg[0] == 'r':
                    # Check if the register is valid
                    if not arg[1:].isdigit() or int(arg[1:]) < 0 or int(arg[1:]) > 7:
                        raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid register:\n\t\t{arg}")
                    arg_states.append(0x00)
                elif arg[0] == 'a':
                    # Check if the RAM address is valid
                    if not arg[1:].isdigit() or int(arg[1:]) < 0 or int(arg[1:]) > 255:
                        raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid RAM address:\n\t\t{arg}")
                    arg_states.append(0x01)
                else:
                    # Check if the argument is a number
                    try:
                        num = int(arg)
                        if num < 0 or num > 255:
                            raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid immediate value:\n\t\t{arg}")
                        arg_states.append(0x02)
                    except ValueError:
                        if num < 0 or num > 255:
                            raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid immediate value:\n\t\t{arg}")
                        raise ValueError(f"Error on line: {self.current_line}.\n\tInvalid argument:\n\t\t{arg}")
        
        arg_metadata = []

        for state in arg_states:
            if state == 0x00: # Register
                raise ValueError(f"Error on line: {self.current_line}.\n\tUnimplemented argument type:\n\t\t{"register"}")
            elif state == 0x01: # RAM address
                addr_bytes, addr_data_bytes, metadata = self.process_address(args[arg_states.index(state)], arg_states.index(state), instr_name)
                self.instructions.append(addr_bytes)
                self.data.append(addr_data_bytes)
                arg_metadata.append(metadata)
            elif state == 0x02: # Immediate value
                later.append(int(args[arg_states.index(state)]))

        # Get the instruction bytes
        instr_bytes, data_bytes = self.process_instruction(instr_obj, arg_states, args, arg_metadata)

        self.instructions.append(instr_bytes)
        self.data.append(data_bytes)
        self.data.append(later)

    def __str__(self):
        return self.assemble(self.input)