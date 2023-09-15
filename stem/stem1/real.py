from stem1.engine import Metric
from stem1.engine import Force
from stem1.engine import Spacetime
from stem1 import constants

@Metric.register("MyMetric", "MyOtherMetric")
class M(Metric):
	def contraction():
		pass
	
	def dilation():
		pass