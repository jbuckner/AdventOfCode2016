#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input.txt')]


class Instruction:
    string = None
    low_destination = None
    high_destination = None

    def __init__(self, string, low_destination, high_destination):
        self.string = string
        self.low_destination = low_destination
        self.high_destination = high_destination


class Output:
    name = None
    chips = []

    def __init__(self, name):
        self.chips = []
        self.name = name

    def __str__(self):
        return 'Output %s' % self.name

    def receive_chip(self, chip):
        print '%s received chip %s' % (self, chip)
        self.chips.append(chip)


class Bot:
    name = None
    high_chip = None
    low_chip = None
    instructions = []

    def __init__(self, name):
        self.name = name
        self.instructions = []
        self.high_chip = None
        self.low_chip = None

    def __str__(self):
        return 'Bot %s' % self.name

    def receive_chip(self, chip):
        # if chip in [61, 17]:

        if self.high_chip:
            if chip > self.high_chip:
                self.low_chip = self.high_chip
                self.high_chip = chip
            else:
                self.low_chip = chip
        else:
            if chip < self.low_chip:
                self.high_chip = self.low_chip
                self.low_chip = chip
            else:
                self.high_chip = chip

        if self.low_chip and self.high_chip:
            if (self.low_chip == 61 and self.high_chip == 17 or
                    self.low_chip == 17 and self.high_chip == 61):
                print '*** %s compared 61 to 17 ***' % self

            self.execute_instructions()

    def add_instruction(self, inst):
        self.instructions.append(inst)
        if self.low_chip and self.high_chip:
            self.execute_instructions()

    def execute_instructions(self):
        for instruction in self.instructions:
            instruction.low_destination.receive_chip(self.low_chip)
            self.low_chip = None

            instruction.high_destination.receive_chip(self.high_chip)
            self.high_chip = None

bots = {}
outputs = {}

for line in INPUTS:
    command = line.split(' ')
    # print line

    if command[0] == 'value':
        value = int(command[1])
        bot_id = command[5]
        if bot_id not in bots:
            bots[bot_id] = Bot(bot_id)
        bots[bot_id].receive_chip(value)

    if command[0] == 'bot':
        bot_id = command[1]
        low_destination_object_type = command[5]
        low_destination_object_id = command[6]
        high_destination_object_type = command[10]
        high_destination_object_id = command[11]

        if bot_id not in bots:
            bots[bot_id] = Bot(bot_id)

        bot = bots[bot_id]

        low_destination_object = None
        high_destination_object = None

        # create the destination outputs and bots if they don't exist
        if high_destination_object_type == 'output':
            if high_destination_object_id not in outputs:
                new_output = Output(high_destination_object_id)
                outputs[high_destination_object_id] = new_output
            high_destination_object = outputs[high_destination_object_id]
        elif high_destination_object_type == 'bot':
            if high_destination_object_id not in bots:
                new_bot = Bot(high_destination_object_id)
                bots[high_destination_object_id] = new_bot
            high_destination_object = bots[high_destination_object_id]

        if low_destination_object_type == 'output':
            if low_destination_object_id not in outputs:
                new_output = Output(low_destination_object_id)
                outputs[low_destination_object_id] = new_output
            low_destination_object = outputs[low_destination_object_id]
        elif low_destination_object_type == 'bot':
            if low_destination_object_id not in bots:
                new_bot = Bot(low_destination_object_id)
                bots[low_destination_object_id] = new_bot
            low_destination_object = bots[low_destination_object_id]

        instruction = Instruction(line, low_destination_object,
                                  high_destination_object)

        bots[bot_id].add_instruction(instruction)

print 'outputs'
for k in outputs:
    print outputs[k].name, outputs[k].chips
