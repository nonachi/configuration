import unittest
import os
import yaml
import struct
from uvm import Assembler, Interpreter

class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.input_file = 'test_program.asm'
        self.output_file = 'test_output.bin'
        self.log_file = 'test_log.yaml'
        self.assembler = Assembler(self.input_file, self.output_file, self.log_file)

    def tearDown(self):
        # Удаление временных файлов после тестов
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_assemble(self):
        # Создание временного файла с инструкциями
        with open(self.input_file, 'w') as f:
            f.write('121 42\n113 5\n36 10\n66 20\n')

        self.assembler.assemble()

        # Проверка бинарного файла
        with open(self.output_file, 'rb') as f:
            data = f.read()
            self.assertEqual(len(data), 20)  # 4 инструкции по 5 байт каждая

        # Проверка лог-файла
        with open(self.log_file, 'r') as f:
            log_data = yaml.safe_load(f)
            self.assertEqual(len(log_data), 4)
            self.assertEqual(log_data[0]['opcode'], 121)
            self.assertEqual(log_data[0]['operand'], 42)

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.binary_file = 'test_output.bin'
        self.memory_range = (0, 10)
        self.output_file = 'test_result.yaml'
        self.interpreter = Interpreter(self.binary_file, self.memory_range, self.output_file)

    def tearDown(self):
        # Удаление временных файлов после тестов
        if os.path.exists(self.binary_file):
            os.remove(self.binary_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_run(self):
        # Создание временного бинарного файла с инструкциями
        with open(self.binary_file, 'wb') as f:
            f.write(struct.pack('<B', 121))
            f.write(struct.pack('<I', 42))
            f.write(struct.pack('<B', 113))
            f.write(struct.pack('<I', 5))
            f.write(struct.pack('<B', 36))
            f.write(struct.pack('<I', 10))
            f.write(struct.pack('<B', 66))
            f.write(struct.pack('<I', 20))

        self.interpreter.run()

        # Проверка выходного файла
        with open(self.output_file, 'r') as f:
            result_memory = yaml.safe_load(f)
            self.assertEqual(len(result_memory), 10)
            self.assertEqual(result_memory[0], 0)

if __name__ == '__main__':
    unittest.main()
