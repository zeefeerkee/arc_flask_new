class ControlByte:

    def __init__(self):
        # Инициализация байта со значением 00000000
        self.byte = 0b00000000

    def _set_bits(self, mask, value):
        # Устанавливает биты в соответствии с маской и значением
        self.byte = (self.byte & ~mask) | (value & mask)
    
    def direction(self, value):
        # Установка направления (первый бит)
        self._set_bits(0b10000000, value << 7)
        # Сброс остальных битов (второй и третий)
        self._set_bits(0b01100000, 0)
    
    def servo(self, value):
        if value:
            # Установка значений серво (второй и третий биты)
            self._set_bits(0b01100000, 0b00100000)
        else:
            self._set_bits(0b01100000, 0b01000000)
        # Сброс остальных битов (первый и последние 5)
        self._set_bits(0b10011111, 0)
    
    def increase(self):
        # Увеличение последних 5 бит
        speed = self.byte & 0b00011111
        speed = (speed + 1) & 0b00011111
        self._set_bits(0b01111111, speed)
    
    def decrease(self):
        # Уменьшение последних 5 бит
        speed = self.byte & 0b00011111
        speed = (speed - 1) & 0b00011111
        self._set_bits(0b01111111, speed)
    
    def get_byte(self):
        return self.byte
    
    def stop(self):
        self.byte = 0b00000000
        