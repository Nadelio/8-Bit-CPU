High Level Abstraction
```c
main() {
  if(RAM[0] == RAM[1]) { } else { }
}
```
Low Level Abstraction
```arm
_start:
  eql a0 a1
  jcz b0e
  jmp b0
b0e:
  nop
b0:
  nop
```
Intermediate Representation
```arm
// eql a0 a1
xor a0 a1
not r0
and 1 r0
// jcz b0e
// jmp b0
mul r0 1
add r0 20
jmp r0
// b0e
nop
// b0
nop
```
Direct Interface
```arm
//init mem
str 0 r0
str 0 r1
str 0 r2
str 0 r3
str 0 r5
str 0 r6
str 0 r7
// a0
str 0 r7
str r8 r0
str r0 r3
// a1
str 1 r7
str r8 r0
str r0 r2
// xor a0 a1
str 5 r1
str r4 r0
// not r0
str r0 r3
str 7 r1
str r4 r0
// and 1 r0
str 1 r2
str 4 r1
str r4 r0
// mul r0 1
str r0 r3
str 1 r2
str 3 r1
str r4 r0
// add r0 20
str r0 r3
str 20 r2
str 2 r1
str r4 r0
// jmp r0
jmp r0
nop
nop
```
Machine Code
```c
|----Instruction----|    |--------Data-------|
|  8  37  38  39   5|    |  0   0   0   0   0|
|  6   7   7  72  51|    |  0   0   0   0   0|
|  7  72  50  37 136|    |  1   0   0   5   0|
| 51  37 136  38  37|    |  0   7   0   1   4|
|136  51  38  37 136|    |  0   0   1   3   0|
| 51  38  37 136 208|    |  0  20   2   0   0|
|  0   0            |    |  0   0            |
```