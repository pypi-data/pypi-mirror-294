import numpy as np
from bren.nn.initialisers.Initialiser import Initialiser


class HeUniform(Initialiser):
	"""
	Returns values taken from a uniform distribution with endpoints `r` and `-r` where `r = (6 / fan_in)` with `fan_in` being the number of inputs
	"""

	def __init__(self, shape, dtype="float32", **kwargs) -> None:
		super().__init__(shape, dtype, **kwargs)

		self.fan_in, self.fan_out = kwargs.get("inout") or shape
		self.r = np.sqrt(6 / self.fan_in)

	def call(self, *args, **kwargs):
		return np.random.uniform(-self.r, self.r, size=self.shape)