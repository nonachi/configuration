import struct
import sys
import yaml

class Assembler:
    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file
        self.instructions = []

    def assemble(self):
        with open(self.input_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    opcode, operand = int(parts[0]), int(parts[1])
                    print(f"Opcode: {opcode}, Operand: {operand}")  # Отладочный вывод
                    self.instructions.append((opcode, operand))

        with open(self.output_file, 'wb') as f:
            for opcode, operand in self.instructions:
                f.write(struct.pack('<B', opcode))
                f.write(struct.pack('<I', operand))

        log_data = [{'opcode': opcode, 'operand': operand} for opcode, operand in self.instructions]
        with open(self.log_file, 'w') as f:
            yaml.dump(log_data, f)

class Interpreter:
    def __init__(self, binary_file, memory_range, output_file):
        self.binary_file = binary_file
        self.memory_range = memory_range
        self.output_file = output_file
        self.memory = [0] * 1024
        self.stack = []

    def run(self):
        with open(self.binary_file, 'rb') as f:
            while True:
                chunk = f.read(5)
                if not chunk:
                    break
                opcode = chunk[0]
                operand = struct.unpack('<I', chunk[1:])[0]
                self.execute_instruction(opcode, operand)

        result_memory = self.memory[self.memory_range[0]:self.memory_range[1]]
        with open(self.output_file, 'w') as f:
            yaml.dump(result_memory, f)

    def execute_instruction(self, opcode, operand):
        print(f"Executing Opcode: {opcode}, Operand: {operand}")
        print(f"Stack before: {self.stack}")
        if opcode == 121:  # Загрузка константы
            self.stack.append(operand)
        elif opcode == 113:  # Чтение значения из памяти
            if self.stack:
                address = self.stack.pop()
                self.stack.append(self.memory[address])
        elif opcode == 36:  # Запись значения в память
            if len(self.stack) >= 2:
                address = self.stack.pop()  # Адрес записи
                value = self.stack.pop()    # Значение для записи
                print(f"Writing {value} to memory address {address}")  # Отладка
                if 0 <= address < len(self.memory):  # Проверка диапазона памяти
                    self.memory[address] = value
                else:
                    print(f"Error: Invalid memory address {address}")
        elif opcode == 66:  # Побитовый циклический сдвиг вправо
            if self.stack:
                value1 = self.stack.pop()
                result = (value1 >> 1) | ((value1 & 1) << 31)
                self.memory[operand] = result
        else:
            raise ValueError(f"Неизвестная команда: {opcode}")
        print(f"Stack after: {self.stack}")
        print(f"Memory state: {self.memory[:10]}")



if __name__ == "__main__":
    args = sys.argv
    if len(args) < 6:
        print("Использование: python script.py <input_file> <binary_file> <log_file> <memory_range_start> <memory_range_end> <output_file>")
        sys.exit(1)

    assembler = Assembler(args[1], args[2], args[3])
    assembler.assemble()

    memory_range = (int(args[4]), int(args[5]))
    interpreter = Interpreter(args[2], memory_range, args[6])
    interpreter.run()
