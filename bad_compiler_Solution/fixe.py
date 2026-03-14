#!/usr/bin/env python3
"""
Fixed .wut language interpreter
Usage: python3 fixed_compiler.py program.wut

.wut Language Reference:
  (N   - push integer N
  %    - add top two values
  #    - negate top
  @    - decrement top
  !    - increment top
  $    - over (copy second-from-top)
  ~    - push 65 ('A')
  ^    - print top as ASCII char (no pop)
  `    - pop top
  &    - while-start (skip to * if top==0)
  *    - while-end (loop back to & if top!=0)
"""
import sys

def run(source):
    stack = []
    i = 0
    loop_stack = []

    while i < len(source):
        c = source[i]

        if c == '~':
            stack.append(65)

        elif c == '(':
            i += 1
            num = ''
            while i < len(source) and source[i].isdigit():
                num += source[i]; i += 1
            stack.append(int(num) if num else 0)
            continue

        elif c == '#':
            stack[-1] = -stack[-1]

        elif c == '%':
            b = stack.pop(); a = stack.pop()
            stack.append(a + b)

        elif c == '@':
            stack[-1] -= 1

        elif c == '!':
            stack[-1] += 1

        elif c == '$':
            # OVER: copy second-from-top
            stack.append(stack[-2])

        elif c == '^':
            # PRINT top of stack as character (no pop)
            print(chr(stack[-1] % 256), end='')

        elif c == '`':
            stack.pop()

        elif c == '&':
            if stack[-1] != 0:
                loop_stack.append(i)
            else:
                depth = 1; i += 1
                while depth > 0:
                    if source[i] == '&': depth += 1
                    elif source[i] == '*': depth -= 1
                    i += 1
                continue

        elif c == '*':
            if stack[-1] != 0:
                i = loop_stack[-1]
            else:
                loop_stack.pop()

        i += 1

    print()  # final newline

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <program.wut>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        run(f.read().replace('\r','').replace('\n',''))
