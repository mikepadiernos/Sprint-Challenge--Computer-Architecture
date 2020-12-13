"""CPU functionality."""
import sys

print(sys.argv)


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        # self.reg[7] = 0xF4
        self.sp = 7
        self.reg[self.sp] = len(self.ram) - 1
        self.pc = 0
        self.running = True
        self.flag = [0] * 8
        self.instructions = {
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'HLT': 0b00000001,
            'MUL': 0b10100010,
            'POP': 0b01000110,
            'PUSH': 0b01000101,
            'CMP': 0b10100111,
            'JMP': 0b01010100,
            'JEQ': 0b01010101,
            'JNE': 0b01010110,
        }

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as file:
            for line in file:
                line_split = line.split('#')
                num = line_split[0].strip()
                if num == '':
                    continue
                try:
                    self.ram_write(address, int(num, 2))
                except:
                    print(f'unable to convert to an integer')
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == self.instructions['MUL']:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == self.instructions['CMP']:
            self.flag = [0] * 8
            reg_a = self.reg[reg_a]
            reg_b = self.reg[reg_b]
            if reg_a < reg_b:
                self.flag[-3] = 1
            if reg_a > reg_b:
                self.flag[-2] = 1
            if reg_a == reg_b:
                self.flag[-1] = 1
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

        while self.running:
            execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(f'{operand_a}, {operand_b}')

            if execute == self.instructions['HLT']:
                # print(f'HLT')
                self.running = False
                self.pc += 1
            elif execute == self.instructions['PRN']:
                # print(f'PRN')
                value = self.reg[operand_a]
                register = self.ram_read(self.pc + 1)
                print(f"The R{register} value is {value}.")
                self.pc += 2
            elif execute == self.instructions['LDI']:
                # print(f'LDI')
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif execute == self.instructions['MUL']:
                print(f'MUL')
                self.alu(execute, operand_a, operand_b)
                self.pc += 3
            elif execute == self.instructions['PUSH']:
                self.reg[self.sp] -= 1
                value = self.reg[operand_a]
                # print(f'PUSH value {value}')
                # self.ram_write(self.reg[self.sp], self.reg[operand_a])
                self.ram_write(self.reg[self.sp], value)
                self.pc += 2
            elif execute == self.instructions['POP']:
                value = self.ram_read(self.reg[self.sp])
                # print(f'POP value {value}')
                # self.reg[operand_a] = self.ram_read(self.reg[self.sp])
                self.reg[operand_a] = value
                self.reg[self.sp] += 1
                self.pc += 2
            elif execute == self.instructions['CMP']:
                # print(f'CMP')
                self.alu(execute, operand_a, operand_b)
                self.pc += 3
            elif execute == self.instructions['JMP']:
                # print(f'JMP')
                self.pc = self.reg[operand_a]
            elif execute == self.instructions['JEQ']:
                # print(f'JEQ')
                if self.flag[-1] == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif execute == self.instructions['JNE']:
                # print(f'JNE')
                if self.flag[-1] == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            else:
                print(f'exiting...')
                sys.exit(1)
