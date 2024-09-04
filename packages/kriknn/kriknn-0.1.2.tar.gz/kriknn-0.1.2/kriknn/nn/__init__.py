import numpy as np
from kriknn.engine.tensor import Tensor

class Linear:
    def __init__(self, features_in, features_out):
        bound = 1 / np.sqrt(features_in)
        self.weight = Tensor.uniform(
            (features_in, features_out), -bound, bound)
        self.bias = Tensor.uniform((features_out,), -bound, bound)

    def __call__(self, x: Tensor) -> Tensor:
        return x @ self.weight + self.bias
