"""CPU functionality."""

import sys

LDI, PRN, HLT, PUSH, POP, CMP, JMP, JEQ, JNE = 0b10000010, 0b01000111, 0b00000001, 0b01000101, 0b01000110, 0b10100111, 0b01010100, 0b01010101, 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """
        Construct a new CPU.
        """
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 7
        self.reg[self.sp] = len(self.ram) - 1
        self.pc = 0
        self.running = True
        self.flag = [0] * 8

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value

    def load(self):
        print("loading self")
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print('insufficient arguments')
            sys.exit(1)

        address = 0

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    line_split = line.split('#')
                    num = line_split[0].strip()
                    if num == '':
                        continue
                    try:
                        self.ram_write(address, int(num, 2))
                    except:
                        print('unable to convert string to integer')
                    address += 1
        except:
            print('file not found')
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        # elif op == "CMP":
        #     cmp_a = self.reg[reg_a]
        #     cmp_b = self.reg[reg_b]
        #     self.flag = [0] * 8
        #     if cmp_a < cmp_b:
        #         self.flag[-3] = 1
        #     if cmp_a > cmp_b:
        #         self.flag[-2] = 1
        #     if cmp_a == cmp_b:
        #         self.flag[-1] = 1
        #     self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        print("running self")
        # print(f"{self.trace}")
        while self.running:
            # print(f"{self.trace}")
            execute = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            self.instructions(execute, op_a, op_b)

    def instructions(self, execute, op_a, op_b):
        if execute == HLT:
            self.running = False
            self.pc += 1
        elif execute == LDI:
            # print("ldi")
            self.reg[op_a] = op_b
            self.pc += 3
        elif execute == PRN:
            # print("prn")
            value = self.reg[op_a]
            register = self.ram_read(self.pc + 1)
            print(f"The value of R{register} is {value}.")
            self.pc += 2
        elif execute == PUSH:
            print("push")
            self.reg[self.sp] -= 1
            value = self.reg[op_a]
            self.ram_write(value, self.reg[self.sp])
            print(f"{value}")
            self.pc += 2
        elif execute == POP:
            print("pop")
            top = self.ram_read(self.reg[self.sp])
            self.reg[op_a] = top
            self.reg[self.sp] += 1
            print(f"{top}")
            self.pc += 2
        # elif execute == CMP:
        #     print("cmp")
        #     self.alu("CMP", op_a, op_b)
        #     self.pc += 3
        elif execute == CMP:
            # print("cmp")
            cmp_a = self.reg[op_a]
            cmp_b = self.reg[op_b]
            if cmp_a < cmp_b:
                self.flag[-3] = 1
            if cmp_a > cmp_b:
                self.flag[-2] = 1
            if cmp_a == cmp_b:
                self.flag[-1] = 1
            self.pc += 3
        elif execute == JMP:
            # print("jump")
            # print(f"{self.trace}")
            self.pc = self.reg[op_a]
        elif execute == JEQ:
            # print("jeq")
            if self.flag[-1] == 1:
                # print(f"flag {self.flag}")
                self.pc = self.reg[op_a]
            else:
                self.pc += 2
        elif execute == JNE:
            # print("jne")
            if self.flag[-1] == 0:
                self.pc = self.reg[op_a]
            else:
                self.pc += 2
        else:
            print("exit?")
            sys.exit(1)
