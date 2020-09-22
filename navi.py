#!/usr/bin/env python3

import math

samplerate = 44100
sample_idx = 0

def sample_time(sample):
    return sample/samplerate

def sin_hz(freq, sample):
    return math.sin(sample_time(sample)*2*math.pi*freq)

def square_hz(freq, sample, wave_range = (-1.0, 1.0)):
    t = sample_time(sample)*freq
    return wave_range[1] if t-math.floor(t) < 0.5 else wave_range[0]

def sawtooth_hz(freq, sample):
    t = sample_time(sample)*freq
    return 2*(t-math.floor(t+0.5))

def triangle_hz(freq, sample):
    t = sample_time(sample)*freq+0.25
    return 2*abs(2*(t-math.floor(t+0.5)))-1

def write_sample(value):
    if type(value) == float:
        value = int(value*0x7fff)
    print(hex(value))

class Emitter:
    def sample(self) -> float:
        return 0.0

class SinEmitter:
    def __init__(self, frequency):
        self.frequency = frequency
    def sample(self):
        return sin_hz(self.frequency, sample_idx)

class SquareEmitter:
    def __init__(self, frequency, wave_range = (-1.0, 1.0)):
        self.frequency = frequency
        wave_range = wave_range 
        self.wave_range = wave_range 
    def sample(self):
        return square_hz(self.frequency, sample_idx, self.wave_range)

class SawEmitter:
    def __init__(self, frequency):
        self.frequency = frequency
    def sample(self):
        return sawtooth_hz(self.frequency, sample_idx)

class TriangleEmitter:
    def __init__(self, frequency):
        self.frequency = frequency
    def sample(self):
        return triangle_hz(self.frequency, sample_idx)

class FunctionEmitter:
    def __init__(self, funtion):
        self.function = function
    def sample(self):
        return function(sample_time(sample_idx))

class BeatEmitter:
    def __init__(self, beat = [1], bpm = 120):
        self.beat = beat
        self.bpm = bpm
    def sample(self):
        return self.beat[int(sample_idx/samplerate*self.bpm/60)%len(self.beat)]
    def length(self):
        return 60/self.bpm*len(self.beat)

'''
class BeatBeat:
    def __init__(self, beat_emitters = []):
        self.beat_emitters = beat_emitters
        self.total_length = sum([b.length() for b in beat_emitters])
    def sample(self):
        t = sample_time(sample_idx)
        t -= 
'''

class EmitterGroup(Emitter):
    def __init__(self, emitters = []):
        self.emitters=emitters
    def sample(self):
        if len(self.emitters) == 0:
            return 0
        return sum([e.sample() for e in self.emitters])/len(self.emitters)

class SinEmitterGroup(EmitterGroup):
    def __init__(self, frequencies = []):
        groups = [SinEmitter(f) for f in frequencies]
        super().__init__(groups)

class SquareEmitterGroup(EmitterGroup):
    def __init__(self, frequencies = []):
        groups = [SquareEmitter(f) for f in frequencies]
        super().__init__(groups)

class SawEmitterGroup(EmitterGroup):
    def __init__(self, frequencies = []):
        groups = [SawEmitter(f) for f in frequencies]
        super().__init__(groups)

class TriangleEmitterGroup(EmitterGroup):
    def __init__(self, frequencies = []):
        groups = [TriangleEmitter(f) for f in frequencies]
        super().__init__(groups)

class MultiplyGroup(EmitterGroup):
    def __init__(self, emitters = []):
        super().__init__(emitters)
    def sample(self):
        if len(self.emitters) == 0:
            return 0
        total = 1.0
        for e in self.emitters:
            total *= e.sample()
        return total
#s = SinGroup([440, 440*2**(2/12) , 440*2**(7/12)])
s = SinEmitterGroup([440, 440*2**(2/12)])
s2 = SinEmitterGroup([440])
s3 = SinEmitterGroup([440*2])
s4 = SinEmitterGroup([440*3])
s5 = SinEmitterGroup([440*4])
t = SquareEmitter(2, (0.1, 1.0))
t2 = BeatEmitter([1.0, 1.0, 0.0], bpm = 840)
e = MultiplyGroup([s, t])
e2 = MultiplyGroup([s2, t2])
g = EmitterGroup([e, e2])
for i in range(int(44100*6)):
    sample_idx = i
    t = i/44100.0*2
    write_sample(0.1*(s2.sample() + s3.sample()/1.2 + s4.sample()/3 + s4.sample()/1.2)*math.exp(-t**(1/2)))
    #*t**2
    #write_sample(sawtooth_hz(440, i))
    #write_sample(sin_hz(440, i))
    #print(sawtooth_hz(440, i))
#print(triangle_hz(440, 0))
'''
print("-"*50+"+\n")
for i in range(100):
    sample_idx = i
    print("-"*int((triangle_hz(880, i)+1)*50)+"+")
'''
