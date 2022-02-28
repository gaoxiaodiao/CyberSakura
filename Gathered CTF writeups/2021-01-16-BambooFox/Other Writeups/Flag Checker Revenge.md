## Flag Checker Revenge
> **Category:** Reverse
> **Description:** 
> **Pad Link:** http://34.87.94.220/pad/reverse-flag-checker-revenge
> **Flag:** flag{4ll_7h3_w4y_70_7h3_d33p357_v4l1d4710n}
---
We are given an ELF executable, so by throwing it into a disassembler and navigating to the main function:

![](https://i.imgur.com/7OLJsNm.png)

It appears that our input (presumably the flag) should be of length `0x2b`, and a (check) function is called on our input which should return 1.

So, the goal is clear: *find an input that makes the check function return 1, and that will input be our flag!*

So, let's check out what the function does:

![](https://i.imgur.com/LwsLMJn.png)

It seems to be performing some check and then... calls another function?

TLDR the function calls a function which calls a function which...... You get the idea. In fact, there are **500 nested functions**.

## References


## Bugs


## Exploit Ideas
To solve this, we need a script that can help us extract all the check functions and parse the instructions into equations that `z3` can solve.

```bash
objdump -M intel -d task > dump_asm.txt
# or if you're on mac
objdump -x86-asm-syntax=intel -d task > dump_asm.txt
```

This dumps the disassembly into a text file we can work with (it would also be helpful to remove other functions as it cleans things up a little).

Then the rest is just writing a script that takes assembly and spits out python expressions (easier said than done XD), and solving them with `z3`.

```bash
$ python main.py
flag{4ll_7h3_w4y_70_7h3_d33p357_v4l1d4710n}
```

## Scripts
```python
import sys
import re
from z3 import *

s = Solver()
flag = []
length = 0x2b
for i in range(length+1):
    flag.append(BitVec(str(i), 8))

dumpfile = './dump_asm.txt'

def extract_instructions():
    with open(dumpfile, 'r') as f:
        data = f.read().split('\n\n')[:-1]
        data = list(map( \
            lambda x: '\n'.join( \
                list(map( \
                    lambda y: y[40:].replace('\t', ' '), \
                    x.split('\n') \
                ))[1:] \
            ), data))

        return data

def has_digit(string):
    return any(c.isdigit() for c in string)

def split_line(line):
    split = line.split(' ')
    # e.g. sar al => sar al, 1
    if len(split) == 2:
        return split[0], split[1], '1'
    return split[0], split[1][:-1], split[2]

def form_index(ind):
    return "flag[%s]" % ind

def get_indices(block):
    indices = [i for i in range(len(block)) if 'mov rax, qword ptr [rbp - 8]' in block[i]]
    answer = []
    for i in indices:
        if block[i+1].startswith('add'):
            answer.append(int(block[i+1].split(' ')[-1]))
        else:
            answer.append(0)
    inst_start = 0
    for i in range(indices[-1]+2, len(block)):
        if not block[i].startswith('mov'):
            inst_start = i
            break
    return answer, inst_start

def parse_equation(ori_block):
    ori_block = ori_block.split('\n')
    # delete code block after the jump that we want to branch into
    for i in range(len(ori_block)):
        if ori_block[i].startswith('test') or ori_block[i].startswith('cmp'):
            ori_block = ori_block[:i+2]
            break

    indices, start_ind = get_indices(ori_block)
    eax = indices[-1]
    edx = indices[0]
    # extracts instructions after setting edx and eax (equation part)
    block = list(filter(lambda x: len(x.strip()) > 0 and not x.startswith('mov'), ori_block[start_ind:]))
    ans = ""
    eqn = ""
    for b in block:
        inst, src, dest = split_line(b)
        src = form_index(eax if 'a' in src else edx)
        dest = ("(%s)&0xff" % dest) if has_digit(dest) else form_index(eax if 'a' in dest else edx)

        if inst == 'cmp':
            ans = dest
            break
        elif inst == 'test':
            ans = 0
            if block[block.index(b)+1].startswith('js'):
                # check for the sign bit in 8 bit numbers
                return "%s > 128" % src
            break
        elif inst == 'sar':
            eqn = "(%s >> %s)&0xff" % (src, dest)
        elif inst == 'shl':
            eqn = "(%s << %s)&0xff" % (src, dest)
        elif inst == 'sub':
            eqn = "(%s - %s)&0xff" % (src, dest)
        elif inst == 'add':
            eqn = "(%s + %s)&0xff" % (src, dest)
        elif inst == 'mul':
            eqn = "(%s * %s)&0xff" % (src, dest)
        elif inst == 'and':
            eqn = "(%s & %s)&0xff" % (src, dest)
        elif inst == 'or':
            eqn = "(%s | %s)&0xff" % (src, dest)
        elif inst == 'xor':
            eqn = "(%s ^ %s)&0xff" % (src, dest)

    if len(eqn) == 0: eqn = src

    return "%s == %s" % (eqn, ans)

# flag should consist of printable characters
for i in range(length):
    s.add(31 < flag[i])
    s.add(flag[i] < 127)

block = extract_instructions()
for b in block:
    eq = parse_equation(b)
    s.add(eval(eq))

s.check()
result = str(s.model()).replace('[', '{').replace(']', '}').replace('=', ':')
ans = eval(result)
for i in range(length):
    print(chr(ans[i]&0xff), end='')
```

Modified https://github.com/jakespringer/angr_ctf/blob/master/solutions/04_angr_symbolic_stack/solve04.py

This script will find the flag. But it will print them out as 64-bit numbers in little-endian. So we need to do `binascii.unhexlify(hex(...)[2:])[::-1]`.

```python
import angr
import claripy
import sys

def main(argv):
  path_to_binary = argv[1]
  project = angr.Project(path_to_binary)

  # For this challenge, we want to begin after the call to scanf. Note that this
  # is in the middle of a function.
  #
  # This challenge requires dealing with the stack, so you have to pay extra
  # careful attention to where you start, otherwise you will enter a condition
  # where the stack is set up incorrectly. In order to determine where after
  # scanf to start, we need to look at the dissassembly of the call and the
  # instruction immediately following it:
  #   sub    $0x4,%esp
  #   lea    -0x10(%ebp),%eax
  #   push   %eax
  #   lea    -0xc(%ebp),%eax
  #   push   %eax
  #   push   $0x80489c3
  #   call   8048370 <__isoc99_scanf@plt>
  #   add    $0x10,%esp
  # Now, the question is: do we start on the instruction immediately following
  # scanf (add $0x10,%esp), or the instruction following that (not shown)?
  # Consider what the 'add $0x10,%esp' is doing. Hint: it has to do with the
  # scanf parameters that are pushed to the stack before calling the function.
  # Given that we are not calling scanf in our Angr simulation, where should we
  # start?
  # (!)
  start_address = 0x409aa7
  initial_state = project.factory.blank_state(addr=start_address)

  # We are jumping into the middle of a function! Therefore, we need to account
  # for how the function constructs the stack. The second instruction of the
  # function is:
  #   mov    %esp,%ebp
  # At which point it allocates the part of the stack frame we plan to target:
  #   sub    $0x18,%esp
  # Note the value of esp relative to ebp. The space between them is (usually)
  # the stack space. Since esp was decreased by 0x18
  #
  #        /-------- The stack --------\
  # ebp -> |                           |
  #        |---------------------------|
  #        |                           |
  #        |---------------------------|
  #         . . . (total of 0x18 bytes)
  #         . . . Somewhere in here is
  #         . . . the data that stores
  #         . . . the result of scanf.
  # esp -> |                           |
  #        \---------------------------/
  #
  # Since we are starting after scanf, we are skipping this stack construction
  # step. To make up for this, we need to construct the stack ourselves. Let us
  # start by initializing ebp in the exact same way the program does.
  initial_state.regs.rbp = initial_state.regs.rsp

  # scanf("%u %u") needs to be replaced by injecting four bitvectors. The
  # reason for this is that Angr does not (currently) automatically inject
  # symbols if scanf has more than one input parameter. This means Angr can
  # handle 'scanf("%u")', but not 'scanf("%u %u")'.
  # You can either copy and paste the line below or use a Python list.
  # (!)
  password = []
  for i in range(9):
    password.append(claripy.BVS('password', 64))

  # Here is the hard part. We need to figure out what the stack looks like, at
  # least well enough to inject our symbols where we want them. In order to do
  # that, let's figure out what the parameters of scanf are:
  #   sub    $0x4,%esp
  #   lea    -0x10(%ebp),%eax
  #   push   %eax
  #   lea    -0xc(%ebp),%eax
  #   push   %eax
  #   push   $0x80489c3
  #   call   8048370 <__isoc99_scanf@plt>
  #   add    $0x10,%esp
  # As you can see, the call to scanf looks like this:
  # scanf(  0x80489c3,   ebp - 0xc,   ebp - 0x10  )
  #      format_string    password0    password1
  #  From this, we can construct our new, more accurate stack diagram:
  #
  #            /-------- The stack --------\
  # ebp ->     |          padding          |
  #            |---------------------------|
  # ebp - 0x01 |       more padding        |
  #            |---------------------------|
  # ebp - 0x02 |     even more padding     |
  #            |---------------------------|
  #                        . . .               <- How much padding? Hint: how
  #            |---------------------------|      many bytes is password0?
  # ebp - 0x0b |   password0, second byte  |
  #            |---------------------------|
  # ebp - 0x0c |   password0, first byte   |
  #            |---------------------------|
  # ebp - 0x0d |   password1, last byte    |
  #            |---------------------------|
  #                        . . .
  #            |---------------------------|
  # ebp - 0x10 |   password1, first byte   |
  #            |---------------------------|
  #                        . . .
  #            |---------------------------|
  # esp ->     |                           |
  #            \---------------------------/
  #
  # Figure out how much space there is and allocate the necessary padding to
  # the stack by decrementing esp before you push the password bitvectors.
  padding_length_in_bytes = 8  # :integer
  initial_state.regs.rsp -= padding_length_in_bytes

  # Push the variables to the stack. Make sure to push them in the right order!
  # The syntax for the following function is:
  #
  # initial_state.stack_push(bitvector)
  #
  # This will push the bitvector on the stack, and increment esp the correct
  # amount. You will need to push multiple bitvectors on the stack.
  # (!)
  for i in range(9):
    initial_state.stack_push(password[i])  # :bitvector (claripy.BVS, claripy.BVV, claripy.BV)

  simulation = project.factory.simgr(initial_state)

  def is_successful(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'win' in stdout_output

  def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'wrong' in stdout_output

  simulation.explore(find=is_successful, avoid=should_abort)

  if simulation.found:
    solution_state = simulation.found[0]

    solutions = []
    for i in range(9):
      solutions.append(solution_state.solver.eval(password[i]))

    solution = ' '.join(map(str, solutions))
    print(solution)
  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)
```