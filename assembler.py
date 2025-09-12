import argparse
import os
from pathlib import Path
import re

def main():
    parser = argparse.ArgumentParser(description="Translate Hack assembly program (.asm) into Hack binary code (.hack)")
    parser.add_argument('-p', '--path', help='path to Hack assembly prgoram (.asm)', required=True)
    args = parser.parse_args()
    path = Path(args.path)
    save_path = f'{path.parent}/{path.stem}.hack'

    JUMP_DICT = {
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }

    COMP_DICT = {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        'M': '1110000',
        '!M': '1110001',
        '-M': '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101',
    }
    
    input_asm = []
    with open(args.path, 'r') as asm_file:
        for line in asm_file:
            input_asm.append(line.strip())
    
    with open(save_path, 'a') as hack_file:
        hack_file.truncate(0)
        for line in input_asm:
            write_line = ''
            if line == '' or line[0:2] == '//': # comment or empty
                continue
            elif line[0] == '@': # a instruction
                write_line = format(int(line[1:]), '016b')
            else: # c instruction
                write_line = ['1'] * 3 + ['0'] * 13
                line = line.split('=')
                if len(line) == 2:
                    dest = line[0]
                    if 'M' in dest:
                        write_line[12] = '1'
                    if 'D' in dest:
                        write_line[11] = '1'
                    if 'A' in dest:
                        write_line[10] = '1'
                    line = [line[1]]

                line = line[0]
                line = line.split(';')
                if len(line) == 2:
                    jmp = line[1]
                    jmp_bin = JUMP_DICT[jmp]
                    for i in range(3):
                        write_line[13 + i] = jmp_bin[i]

                comp = line[0]
                comp_bin = COMP_DICT[comp]
                for i in range(7):
                    write_line[3 + i] = comp_bin[i]

                write_line = ''.join(write_line)

            hack_file.write(write_line + '\n')



if __name__ == "__main__":
    main()