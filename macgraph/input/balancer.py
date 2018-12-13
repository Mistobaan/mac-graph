
import random
import math
from collections import Counter

import logging
logger = logging.getLogger(__name__)

class Balancer(object):
	"""
	It's the caller's duty to close record_writer
	"""

	def __init__(self, record_writer, balance_freq, name="", parent=None):
		self.batch_i = 0
		self.record_writer = record_writer
		self.balance_freq = balance_freq
		self.name = name
		self.parent = parent
		self.running_total = None
		self.answer_classes = Counter()
		self.answer_classes_types = Counter()
		self.written = 0

	def oversampled_so_far(self):
		raise NotImplementedException()

	def oversample(self, n):
		'''Return over-sampling with n items total'''
		raise NotImplementedException()

	def write(self, doc, item):

		key = (str(doc["answer"]), doc["question"]["type_string"])
		self.answer_classes[str(doc["answer"])] += 1
		self.answer_classes_types[key] += 1
		self.written += 1

		# Only do this for top level class
		if self.parent is None:
			self.batch_i += 1
			self.pipe_if_ready()

	def pipe(self):
		for i in self.oversample(self.batch_i):
			self.record_writer.write(*i)

	def pipe_if_ready(self):
		if self.batch_i > self.balance_freq:
			self.pipe()
			self.batch_i = 0

	def __enter__(self):
		return self

	def __exit__(self, *vargs):
		if self.parent is None:
			self.pipe()
			print(self.running_total)


def resample_list(l, n):
	if n < 0:
		raise ArgumentError("Cannot sample list to negative size")
	elif n == 0:
		r = []
	elif n == len(l):
		r = l
	elif n >= len(l):
		r = l + [random.choice(l) for i in range(n - len(l))]
	else:
		r = random.sample(l, n)

	assert len(r) == n
	return r


class ListBalancer(Balancer):

	def __init__(self, record_writer, balance_freq, name="", parent=None):
		super().__init__(record_writer, balance_freq, name, parent)
		self.data = []

	def write(self, doc, item):
		self.data.append((doc,item))
		self.data = self.data[-self.balance_freq:]
		super().write(doc, item)

	def oversample(self, n):
		if len(self.data) == 0:
			raise ValueError("Cannot sample empty list")
		
		r = resample_list(self.data, n)
		return r


class DictBalancer(Balancer):

	def __init__(self, key_pred, CtrClzz, record_writer, balance_freq, name="", parent=None):
		super().__init__(record_writer, balance_freq, name, parent)
		self.data = {}
		self.key_pred = key_pred
		self.CtrClzz = CtrClzz
		self.running_total = Counter()

	def write(self, doc, item):
		key = self.key_pred(doc)

		if key not in self.data:
			self.data[key] = self.CtrClzz(self.record_writer, self.balance_freq, key, self)

		if key not in self.running_total:
			self.running_total[key] = 0

		self.data[key].write(doc, item)
		super().write(doc, item)

	def oversampled_so_far(self):
		return sum(self.running_total.values())

	def oversample(self, n):

		total_target = self.oversampled_so_far() + n

		if len(self.data) > 0:
			target_per_class = math.ceil(total_target / len(self.data))
		else:
			logger.warning(f"Oversample called on {self.name} but no data added")
			return []

		if n <= 0:
			return []

		r = []

		for k, v in self.running_total.items():
			o = self.data[k].oversample(target_per_class - v)
			o = [(k, i) for i in o]
			r.extend(o)

		r = resample_list(r, n)

		classes, r = zip(*r) # aka unzip
		self.running_total.update(classes)

		assert len(r) == n, f"DictBalancer {self.name} tried to return {len(r)} not {n} items"
		assert sum(self.running_total.values()) == total_target
		return r


class TwoLevelBalancer(DictBalancer):
	def __init__(self, key1, key2, record_writer, balance_freq, name="TwoLevelBalancer", parent=None):
		Inner = lambda record_writer, balance_freq, name, parent: DictBalancer(key2, ListBalancer, record_writer, balance_freq, name, parent)
		super().__init__(key1, Inner, record_writer, balance_freq, name, parent)

