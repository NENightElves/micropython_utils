from machine import Pin
import time


class C_74HC595:

    def __init__(self, SER, SCK, RCK, CE=None, amount=1, delay=10):
        self.SER = Pin(SER, Pin.OUT)
        self.SCK = Pin(SCK, Pin.OUT)
        self.RCK = Pin(RCK, Pin.OUT)
        if CE:
            self.CE = Pin(CE, Pin.OUT)
        else:
            self.CE = None
        self.amount = amount
        self.datalength = amount*8
        self.delay = delay

    def write(self, l: list):
        if len(l) > self.datalength:
            raise Exception('length error')
        for _ in l:
            if _ != 0 and _ != 1:
                raise Exception('value error')
        for _ in l:
            self.SCK.off()
            time.sleep_us(self.delay)
            self.SER.value(_)
            time.sleep_us(self.delay)
            self.SCK.on()
            time.sleep_us(self.delay)
        for _ in range(0, self.datalength-len(l)):
            self.SCK.off()
            time.sleep_us(self.delay)
            self.SER.value(0)
            time.sleep_us(self.delay)
            self.SCK.on()
            time.sleep_us(self.delay)
        self.RCK.off()
        time.sleep_us(self.delay)
        self.RCK.on()

    def enable(self):
        if self.CE:
            self.CE.off()

    def disable(self):
        if self.CE:
            self.CE.on()


class C_74HC165:

    def __init__(self, Q7, CP, PL, CE=None, amount=1, delay=10):
        self.Q7 = Pin(Q7, Pin.IN)
        self.CP = Pin(CP, Pin.OUT)
        self.PL = Pin(PL, Pin.OUT)
        if CE:
            self.CE = Pin(CE, Pin.OUT)
        else:
            self.CE = None
        self.amount = amount
        self.datalength = amount*8
        self.delay = delay

    def read(self) -> list:
        r = []
        self.CP.on()
        time.sleep_us(self.delay)
        self.PL.off()
        time.sleep_us(self.delay)
        self.PL.on()
        time.sleep_us(self.delay)
        for _ in range(0, self.amount):
            l = []
            for __ in range(0, 8):
                self.CP.off()
                time.sleep_us(self.delay)
                l.append(self.Q7.value())
                time.sleep_us(self.delay)
                self.CP.on()
                time.sleep_us(self.delay)
            l.reverse()
            r.extend(l)
        return r

    def enable(self):
        if self.CE:
            self.CE.off()

    def disable(self):
        if self.CE:
            self.CE.on()
