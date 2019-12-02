class Instructions:


    instructions = {'0A': {'instruction': 'ASL', 'AMOD': 'A'},
    '06': {'instruction': 'ASL', 'AMOD': 'oper'},
    '16': {'instruction': 'ASL', 'AMOD': 'oper'},
    '0E': {'instruction': 'ASL', 'AMOD': 'oper'},
    '1E': {'instruction': 'ASL', 'AMOD': 'oper'},
    '00': {'instruction': 'BRK', 'AMOD': 'impl'},
    '18': {'instruction': 'CLC', 'AMOD': 'impl'},
    'D8': {'instruction': 'CLD', 'AMOD': 'impl'},
    '58': {'instruction': 'CLI', 'AMOD': 'impl'},
    'B8': {'instruction': 'CLV', 'AMOD': 'impl'},
    'CA': {'instruction': 'DEX', 'AMOD': 'impl'},
    '88': {'instruction': 'DEY', 'AMOD': 'impl'},
    'E8': {'instruction': 'INX', 'AMOD': 'impl'},
    'C8': {'instruction': 'INY', 'AMOD': 'impl'},
    '4A': {'instruction': 'LSR', 'AMOD': 'A'},
    '46': {'instruction': 'LSR', 'AMOD': 'oper'},
    '56': {'instruction': 'LSR', 'AMOD': 'oper'},
    '4E': {'instruction': 'LSR', 'AMOD': 'oper'},
    '5E': {'instruction': 'LSR', 'AMOD': 'oper'},
    'EA': {'instruction': 'NOP', 'AMOD': 'impl'},
    '48': {'instruction': 'PHA', 'AMOD': 'impl'},
    '08': {'instruction': 'PHP', 'AMOD': 'impl'},
    '68': {'instruction': 'PLA', 'AMOD': 'impl'},
    '28': {'instruction': 'PLP', 'AMOD': 'impl'},
    '2A': {'instruction': 'ROL', 'AMOD': 'A'},
    '26': {'instruction': 'ROL', 'AMOD': 'oper'},
    '36': {'instruction': 'ROL', 'AMOD': 'oper'},
    '2E': {'instruction': 'ROL', 'AMOD': 'oper'},
    '3E': {'instruction': 'ROL', 'AMOD': 'oper'},
    '6A': {'instruction': 'ROR', 'AMOD': 'A'},
    '66': {'instruction': 'ROR', 'AMOD': 'oper'},
    '76': {'instruction': 'ROR', 'AMOD': 'oper'},
    '6E': {'instruction': 'ROR', 'AMOD': 'oper'},
    '7E': {'instruction': 'ROR', 'AMOD': 'oper'},
    '38': {'instruction': 'SEC', 'AMOD': 'impl'},
    'F8': {'instruction': 'SED', 'AMOD': 'impl'},
    '78': {'instruction': 'SEI', 'AMOD': 'impl'},
    'AA': {'instruction': 'TAX', 'AMOD': 'impl'},
    'A8': {'instruction': 'TAY', 'AMOD': 'impl'},
    'BA': {'instruction': 'TSX', 'AMOD': 'impl'},
    '8A': {'instruction': 'TXA', 'AMOD': 'impl'},
    '9A': {'instruction': 'TXS', 'AMOD': 'impl'},
    '98': {'instruction': 'TYA', 'AMOD': 'impl'},
#below are all instructions for C grade
    '69': {'instruction': 'ADC', 'AMOD': '#'},
    '65': {'instruction': 'ADC', 'AMOD': 'zpg'},
    '29': {'instruction': 'AND', 'AMOD': '#'},
    '25': {'instruction': 'AND', 'AMOD': 'zpg'},
    '06': {'instruction': 'ASL', 'AMOD': 'zpg'},
    'C9': {'instruction': 'CMP', 'AMOD': '#'},
    'C5': {'instruction': 'CMP', 'AMOD': 'zpg'},
    'E0': {'instruction': 'CPX', 'AMOD': '#'},
    'E4': {'instruction': 'CPX', 'AMOD': 'zpg'},
    'C0': {'instruction': 'CPY', 'AMOD': '#'},
    'C4': {'instruction': 'CPY', 'AMOD': 'zpg'},
    'C6': {'instruction': 'DEC', 'AMOD': 'zpg'},
    '49': {'instruction': 'EOR', 'AMOD': '#'},
    '45': {'instruction': 'EOR', 'AMOD': 'zpg'},
    'E6': {'instruction': 'INC', 'AMOD': 'zpg'},
    'A9': {'instruction': 'LDA', 'AMOD': '#'},
    'A5': {'instruction': 'LDA', 'AMOD': 'zpg'},
    'A2': {'instruction': 'LDX', 'AMOD': '#'},
    'A6': {'instruction': 'LDX', 'AMOD': 'zpg'},
    'A0': {'instruction': 'LDY', 'AMOD': '#'},
    'A4': {'instruction': 'LDY', 'AMOD': 'zpg'},
    '46': {'instruction': 'LSR', 'AMOD': 'zpg'},
    '09': {'instruction': 'ORA', 'AMOD': '#'},
    '05': {'instruction': 'ORA', 'AMOD': 'zpg'},
    '26': {'instruction': 'ROL', 'AMOD': 'zpg'},
    '66': {'instruction': 'ROR', 'AMOD': 'zpg'},
    'E9': {'instruction': 'SBC', 'AMOD': '#'},
    'E5': {'instruction': 'SBC', 'AMOD': 'zpg'},
    '85': {'instruction': 'STA', 'AMOD': 'zpg'},
    '86': {'instruction': 'STX', 'AMOD': 'zpg'},
    '84': {'instruction': 'STY', 'AMOD': 'zpg'},

    #below are all for a B
    '6D': {'instruction': 'ADC', 'AMOD': 'abs'},
    '2D': {'instruction': 'AND', 'AMOD': 'abs'},
    '0E': {'instruction': 'ASL', 'AMOD': 'abs'},
    '90': {'instruction': 'BCC', 'AMOD': 'rel'},
    '84': {'instruction': 'BCS', 'AMOD': 'rel'},
    'F0': {'instruction': 'BEQ', 'AMOD': 'rel'},
    '2C': {'instruction': 'BIT', 'AMOD': 'abs'},
    '30': {'instruction': 'BMI', 'AMOD': 'rel'},
    'D0': {'instruction': 'BNE', 'AMOD': 'rel'},
    '10': {'instruction': 'BPL', 'AMOD': 'rel'},
    '50': {'instruction': 'BVC', 'AMOD': 'rel'},
    '70': {'instruction': 'BVS', 'AMOD': 'rel'},
    'CD': {'instruction': 'CMP', 'AMOD': 'abs'},
    'EC': {'instruction': 'CPX', 'AMOD': 'abs'},
    'CC': {'instruction': 'CPY', 'AMOD': 'abs'},
    'CE': {'instruction': 'DEC', 'AMOD': 'abs'},
    '4D': {'instruction': 'EOR', 'AMOD': 'abs'},
    'EE': {'instruction': 'INC', 'AMOD': 'abs'},
    '4C': {'instruction': 'JMP', 'AMOD': 'abs'},
    '20': {'instruction': 'JSR', 'AMOD': 'abs'},
    'AD': {'instruction': 'LDA', 'AMOD': 'abs'},
    'AE': {'instruction': 'LDX', 'AMOD': 'abs'},
    'AC': {'instruction': 'LDY', 'AMOD': 'abs'},
    '4E': {'instruction': 'LSR', 'AMOD': 'abs'},
    '0D': {'instruction': 'ORA', 'AMOD': 'abs'},
    '2E': {'instruction': 'ROL', 'AMOD': 'abs'},
    '6E': {'instruction': 'ROR', 'AMOD': 'abs'},
    '60': {'instruction': 'RTS', 'AMOD': 'impl'},
    'ED': {'instruction': 'SBC', 'AMOD': 'abs'},
    '8D': {'instruction': 'STA', 'AMOD': 'abs'},
    '8E': {'instruction': 'STX', 'AMOD': 'abs'},
    '8C': {'instruction': 'STY', 'AMOD': 'abs'}}