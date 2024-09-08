
import numpy as np

from .qubit import QubitCollection
from . import operations
from . import reggate

from collections import deque
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING: from .operations import QuantumOperation


class QuantumRegister:
    transform: 'QuantumOperation'

    def __init__(self, transform: 'QuantumOperation'):
        self.transform = transform
        self.transform.initiate()

    def __del__(self):
        self.transform.finalize()

    def __invert__(self):
        return QuantumRegister(operations.BitNotOperation(self.transform))
    
    def copy(self):
        return QuantumRegister(operations.CopyOperation(self.transform))

    def __and__(self, other: 'QuantumRegister') -> 'QuantumRegister':
        return QuantumRegister(operations.BitAndOperation(self.transform, other.transform))

    def __or__(self, other: 'QuantumRegister') -> 'QuantumRegister':
        return QuantumRegister(operations.BitOrOperation(self.transform, other.transform))

    def __eq__(self, value: 'QuantumRegister | int') -> 'QuantumRegister':
        if isinstance(value, int):
            return QuantumRegister(operations.EqualImmediateOperation(self.transform, value))
        
        # return QuantumRegister(operations.EqualOperation(self.transform, value.transform))
        raise NotImplementedError("Equality comparison between two quantum registers is not yet implemented")

    def __xor__(self, other: 'QuantumRegister') -> 'QuantumRegister':
        return QuantumRegister(operations.BitXorOperation(self.transform, other.transform))

    def __add__(self, other: 'QuantumRegister|int') -> 'QuantumRegister':
        if isinstance(other, int):
            return QuantumRegister(operations.AddImmediateOperation(self.transform, other))
        return QuantumRegister(operations.AddOperation(self.transform, other.transform))
    
    def __sub__(self, other: 'QuantumRegister|int') -> 'QuantumRegister':
        if isinstance(other, int):
            return QuantumRegister(operations.SubImmediateOperation(self.transform, other))
        return QuantumRegister(operations.SubOperation(self.transform, other.transform))

    def __mul__(self, other: 'QuantumRegister') -> 'QuantumRegister':
        return QuantumRegister(operations.MultiplyOperation(self.transform, other.transform))

    def __int__(self) -> int:
        return reggate.measure(self.transform.reg)
    
    def __bool__(self) -> bool:
        return bool(int(self))
    
    def __str__(self) -> str:
        return str(int(self))
    
