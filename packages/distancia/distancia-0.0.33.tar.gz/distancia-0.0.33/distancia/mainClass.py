from abc import ABC   # permet de définir des classes de base

class Distance(ABC):
	obj1_exemple=[1, 2, 3]
	obj2_exemple=[4, 5, 6]
	type1=list
	type2=list
	
	def __call__(self,*args):
		if len(args)==2:
			return self.distance_function(args[0], args[1])
		if len(args)==3:
			return self.distance_function(args[0], args[1], args[2])
		if len(args)==4:
			return self.distance_function(args[0], args[1], args[2], args[3])
		
	def calculate(self,*args):
	#def distance(self, obj1, obj2):
		"""
		Calculate the distance between two objects.
		:param obj1: First object
		:param obj2: Second object
		....
		:return: Distance between obj1, obj2, ...
		"""
		if len(args)==2:
			return self.distance_function(args[0], args[1])
		if len(args)==3:
			return self.distance_function(args[0], args[1], args[2])
		if len(args)==4:
			return self.distance_function(args[0], args[1], args[2], args[3])

	def check_data(self, obj1, obj2):
		"""
		Verify the data of a distance measure: type, dimension.
		"""
		
		print(type(obj1))
		print(self.type1)
		properties = {
				f'collection1_type {self.type1}': type(obj1) is self.type1,
				f'collection2_type {self.type2}': type(obj2) is self.type2,
				f'data_type': True and True,
				f'association_rules': True and True,
		}
		print(f"Data verification: {properties}")
		
	def check_properties(self, obj1, obj2, obj3):
		"""
		Verify the properties of a distance measure: non-negativity, identity of indiscernibles, symmetry, and triangle inequality.
		:param obj1: First object
		:param obj2: Second object
		:param obj3: Third object
		:return: Dictionary indicating whether each property holds
		"""
		d12 = self.calculate(obj1, obj2)
		d13 = self.calculate(obj1, obj3)
		d23 = self.calculate(obj2, obj3)

		properties = {
				'non_negativity': d12 >= 0 and d13 >= 0 and d23 >= 0,
				'identity_of_indiscernibles': (d12 == 0) == (obj1 == obj2) and (d13 == 0) == (obj1 == obj3) and (d23 == 0) == (obj2 == obj3),
				'symmetry': d12 == self.calculate(obj2, obj1) and d13 == self.calculate(obj3, obj1) and d23 == self.calculate(obj3, obj2),
				'triangle_inequality': d12 <= d13 + d23 and d13 <= d12 + d23 and d23 <= d12 + d13,
		}
		print(f"Properties verification: {properties}")

	def exemple(self):
		# Example usage
		if not hasattr(self, 'obj3_exemple')and not hasattr(self, 'obj4_exemple'):
			print(f"{self.__class__.__name__} distance between {self.obj1_exemple} and {self.obj2_exemple} is {self.calculate(self.obj1_exemple, self.obj2_exemple):.2f}")
		elif not hasattr(self, 'obj4_exemple'):
			print(f"{self.__class__.__name__} distance {self.obj3_exemple} between {self.obj1_exemple} and {self.obj2_exemple} is {self.calculate(self.obj1_exemple, self.obj2_exemple, self.obj3_exemple):.2f}")
		else:
			print(f"{self.__class__.__name__} distance {self.obj3_exemple}, {self.obj4_exemple} between {self.obj1_exemple} and {self.obj2_exemple} is {self.calculate(self.obj1_exemple, self.obj2_exemple, self.obj3_exemple, self.obj4_exemple):.2f}")
