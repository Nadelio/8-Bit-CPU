# 8-Bit CPU Assembly Instructions

This document contains a set of unique assembly instructions that operate every part of the CPU, including ALU operations, register operations, and memory interactions. Each instruction is annotated with its corresponding CPU bytecode.

---

## ALU Operations
These operations are controlled by the ALU OP Register (`r1`), which determines the operation performed by the ALU.

| Assembly Instruction | Bytecode | Explanation |
|-----------------------|----------|-------------|
| `NOP`                | `0`      | No operation. |
| `SUB`                | `1`      | Subtracts the operand register from the accumulator. |
| `ADD`                | `2`      | Adds the operand register to the accumulator. |
| `MUL`                | `3`      | Multiplies the operand register with the accumulator. |
| `AND`                | `4`      | Performs a bitwise AND operation between the operand register and the accumulator. |
| `XOR`                | `5`      | Performs a bitwise XOR operation between the operand register and the accumulator. |
| `OR`                 | `6`      | Performs a bitwise OR operation between the operand register and the accumulator. |
| `NOT`                | `7`      | Performs a bitwise NOT operation on the accumulator. |

---

## Register Operations
These instructions store values into specific registers or read values from them.

| Assembly Instruction | Bytecode | Explanation |
|-----------------------|----------|-------------|
| `STR_R0`             | `8`      | Stores the value from the operand register into the output register (`r0`). |
| `STR_R1`             | `37`     | Stores the value from the operand register into the ALU operand register (`r1`). |
| `STR_R2`             | `38`     | Stores the value from the operand register into the ALU low register (`r2`). |
| `STR_R3`             | `39`     | Stores the value from the operand register into the ALU high register (`r3`). |
| `STR_R5`             | `5`      | Stores the value from the operand register into the RAM operand register (`r5`). |
| `STR_R6`             | `6`      | Stores the value from the operand register into the RAM low register (`r6`). |
| `STR_R7`             | `7`      | Stores the value from the operand register into the RAM high register (`r7`). |

---

## Memory and Data Operations
These instructions handle reading from and writing to memory and registers, as well as jumping to specific addresses.

| Assembly Instruction | Bytecode | Explanation |
|-----------------------|----------|-------------|
| `READ_R0`            | `16`     | Reads the value from the output register (`r0`) into the accumulator. |
| `READ_R4`            | `128`    | Reads the value from the ALU output register (`r4`) into the accumulator. |
| `READ_R8`            | `64`     | Reads the value from the RAM output register (`r8`) into the accumulator. |
| `JMP_STATIC`         | `192`    | Sets the program counter to a static address provided in the instruction. |
| `JMP_DYNAMIC`        | `208`    | Sets the program counter to the address stored in the output register (`r0`). |

---

## Combined Operations
These instructions combine store and read operations for efficiency.

| Assembly Instruction | Bytecode | Explanation |
|-----------------------|----------|-------------|
| `STR_READ_R0`        | `24`     | Stores a value into the output register (`r0`) and immediately reads it back into the accumulator. |
| `STR_READ_R4`        | `165`    | Stores a value into the ALU operand register (`r1`) and immediately reads the ALU output register (`r4`). |
| `STR_READ_R8`        | `69`     | Stores a value into the RAM operand register (`r5`) and immediately reads the RAM output register (`r8`). |

---
## Explanation of Bytecode Calculation
1. `str` Instructions:
    - Bytecode is calculated as `4 + <dist> + <reg?>`, except when storing to the output register (`r0`), where it is `8 + <reg>`.

2. `read` Instructions:
    - Bytecode depends on the source:
      - `READ_R0`: `16`
      - `READ_R4`: `128`
      - `READ_R8`: `64`

3. `jmp` Instructions:
    - Static jump: `192`
    - Dynamic jump: `192 + 16 = 208`

4. ALU Operations:
   - Controlled by the ALU OP Register (`r1`), with values `0` to `7` corresponding to the operations listed above.

---

## Example Program
This program demonstrates how to implement the provided C-like logic (`if (RAM[0] == RAM[1]) {}`) using the assembly instructions.

### Assembly Code
```asm
// Initialize memory
str 0 r0       // Clear output register
str 0 r1       // Clear ALU OP register
str 0 r2       // Clear ALU Low register
str 0 r3       // Clear ALU High register
str 0 r5       // Clear RAM OP register
str 0 r6       // Clear RAM Low register
str 0 r7       // Clear RAM High register

// Load RAM[0] into ALU High Register (r3)
str 0 r7       // Set RAM address to 0
read r8 r0     // Read RAM[0] into r0
str r0 r3      // Store r0 into ALU High Register (r3)

// Load RAM[1] into ALU Low Register (r2)
str 1 r7       // Set RAM address to 1
read r8 r0     // Read RAM[1] into r0
str r0 r2      // Store r0 into ALU Low Register (r2)

// XOR RAM[0] and RAM[1]
str 5 r1       // Set ALU operation to XOR
read r4 r0     // Read ALU output into r0

// NOT the result
str r0 r3      // Store r0 into ALU High Register (r3)
str 7 r1       // Set ALU operation to NOT
read r4 r0     // Read ALU output into r0

// AND the result with 1
str 1 r2       // Store 1 into ALU Low Register (r2)
str 4 r1       // Set ALU operation to AND
read r4 r0     // Read ALU output into r0

// Multiply the result by 1
str r0 r3      // Store r0 into ALU High Register (r3)
str 1 r2       // Store 1 into ALU Low Register (r2)
str 3 r1       // Set ALU operation to MUL
read r4 r0     // Read ALU output into r0

// Add 20 to the result
str r0 r3      // Store r0 into ALU High Register (r3)
str 20 r2      // Store 20 into ALU Low Register (r2)
str 2 r1       // Set ALU operation to ADD
read r4 r0     // Read ALU output into r0

// Jump to the "if" branch if r0 != 0
jmp r0         // Jump to the address in r0
nop            // No operation (padding)
nop            // No operation (padding)

// Else branch
str 0 r0       // Clear output register (else branch logic)
```

---

This set of instructions ensures that every part of the CPU is utilized, covering ALU operations, register interactions, and memory operations.