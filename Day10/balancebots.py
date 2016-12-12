#!/usr/bin/env python

INPUTS = [line.rstrip('\n') for line in open('input2.txt')]


class Instructable:
    instructions = []

    def receive_instruction(self, instruction):
        self.instructions.append(instruction)

    def execute_instructions(self):
        pass


class ValueReceiver:
    chips = []

    def receive_value(self, chip):
        self.chips.append(chip)


class ValueSender:
    def send_value_to_target(self, chip, target):
        if callable(target.receive_value):
            target.receive_value(chip)


class Output(ValueReceiver):
    pass


class Input(ValueSender):
    def send_value_to_target(self, high_or_low, target):
        if callable(target.receive_value):
            target.receive_value(high_or_low)


class Bot(ValueReceiver, ValueSender, Instructable):
    name = None
    high_chip = None
    low_chip = None

    def receive_chip(self, chip):
        assert self.low_chip and self.high_chip, 'chips full'

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
            self.execute_instructions()

    def send_high_or_low_chip_to_target(self, high_or_low, target):
        assert high_or_low in ['high', 'low'], '`high` or `low`'
        assert callable(target.receive_value), 'target needs `def receive_value`'

        if high_or_low == 'high':
            target.receive_value(self.high_chip)
            self.high_chip = None
        else:
            target.receive_value(self.low_chip)
            self.low_chip = None

    def send_chip_with_value_to_target(self, chip_value, target):
        assert callable(target.receive_value), 'target needs `def receive_value`'

        if self.high_chip == chip_value:
            target.receive_value(self.high_chip)
            self.high_chip = None
        elif self.low_chip == chip_value:
            target.receive_value(self.low_chip)
            self.low_chip = None

bots = []


for line in INPUTS:
    command = line.split(' ')
    if command[0] == 'value':
        value = int(command[1])
        bot = command[5]
        for bot in bots:
            bot_found = False
            if bot.name == bot:
                bot.receive_chip(value)
                bot_found = True
        if not bot_found:
            new_bot = Bot()
            new_bot.receive_chip(value)

    if command[0] == 'bot':
        value = int(command[1])
        bot = command[5]
