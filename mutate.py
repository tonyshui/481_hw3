import ast
import astor
import sys
import random
import math
import copy

#Find all the nodes in the program and record them.
class Collector(ast.NodeVisitor):
	def __init__(self):
		self.binop_count = 0
		self.binops_to_visit = []
		self.assign_count = 0
		self.assign_to_visit = []
		self.compare_count = 0
		self.compare_to_visit = []
		# self.boolop_count = 0
		# self.boolops_to_visit = []
		#self.function_count = 0

	def visit_Assign(self, node):
		self.generic_visit(node)
		self.assign_count += 1
		self.assign_to_visit.append(self.assign_count)

	def visit_Compare(self, node):
		self.generic_visit(node)
		for op in range(len(node.ops)):
			self.compare_count += 1
			if (isinstance(node.ops[op], ast.Eq)
				or isinstance(node.ops[op], ast.NotEq)
				or isinstance(node.ops[op], ast.Lt)
				or isinstance(node.ops[op], ast.LtE)
				or isinstance(node.ops[op], ast.Gt)
				or isinstance(node.ops[op], ast.GtE)):
				self.compare_to_visit.append(self.compare_count)

	# This function will get called on every BinOp node in the tree.
	def visit_BinOp(self, node):
		self.generic_visit(node)
		self.binop_count += 1

		if (isinstance(node.op, ast.Add)
			or isinstance(node.op, ast.Sub)
			or isinstance(node.op, ast.Mult)
			or isinstance(node.op, ast.Div)
			or isinstance(node.op, ast.FloorDiv)):
			# record which node we're looking at by using the counter we
			# increment each time we visit a BinOp. This uniquely identifies
			# Add nodes since the AST is traversed deterministically using the
			# visitor pattern
			self.binops_to_visit.append(self.binop_count)




class RewriteNegateOperation(ast.NodeTransformer): #subclass of NodeTransformer
	def __init__(self, count_of_node_to_mutate):
		self.compare_count = 0
		self.count_of_node_to_mutate = count_of_node_to_mutate

	def Random_Compare(self):
		random_int = random.randint(0,5)
		if random_int == 0:
			return ast.Eq()
		elif random_int == 1:
			return ast.NotEq()
		elif random_int == 2:
			return ast.Gt()
		elif random_int == 3:
			return ast.Lt()
		elif random_int == 4:
			return ast.GtE()
		else:
			return ast.LtE()

	def NegateOperation(self, node):
		for op in range(len(node.ops)):
			if(isinstance(node.ops[op], ast.Eq)):
				node.ops[op] = self.Random_Compare()
			elif (isinstance(node.ops[op], ast.NotEq)):
				node.ops[op] = self.Random_Compare()
			elif (isinstance(node.ops[op], ast.Lt)):
				node.ops[op] = self.Random_Compare()
			elif (isinstance(node.ops[op], ast.Gt)):
				node.ops[op] = self.Random_Compare()
			elif (isinstance(node.ops[op], ast.LtE)):
				node.ops[op] = self.Random_Compare()
			elif (isinstance(node.ops[op], ast.GtE)):
				node.ops[op] = self.Random_Compare()
			# elif (isinstance(node.ops[op], ast.Is)):
			# 	node.ops[op] = ast.IsNot()
			# elif (isinstance(node.ops[op], ast.IsNot)):
			# 	node.ops[op] = ast.Is()
			# elif (isinstance(node.ops[op], ast.In)):
			# 	node.ops[op] = ast.NotIn()
			# elif (isinstance(node.ops[op], ast.NotIn)):
			# 	node.ops[op] = ast.In()

	def visit_Compare(self, node):
		self.generic_visit(node)
		for op in range(len(node.ops)):
			self.compare_count += 1
			#print(type(node.ops[op]))
			if(self.compare_count == self.count_of_node_to_mutate):
				new_node = copy.deepcopy(node)
				self.NegateOperation(new_node)
				return new_node
			else:
				return node

class SwapOperation(ast.NodeTransformer):
	def __init__(self, count_of_node_to_mutate):
		self.binop_count = 0
		self.count_of_node_to_mutate = count_of_node_to_mutate

	def swap_Op(self, node):
		if(isinstance(node.op, ast.Add)): #BinOp
			node.op = ast.Sub()
		elif(isinstance(node.op, ast.Sub)): #BinOp
			node.op = ast.Add()
		elif(isinstance(node.op, ast.Mult)): #BinOp
			node.op = ast.Div()
		elif(isinstance(node.op, ast.Div)): #BinOp
			node.op = ast.Mult()
		elif(isinstance(node.op, ast.FloorDiv)): #BinOp
			node.op = ast.Div()
		# elif(isinstance(node.op, ast.And)): #BoolOp
		# 	node.op = ast.Or()
		# elif(isinstance(node.op, ast.Or)): #BoolOp
		# 	node.op = ast.And()
		# elif(isinstance(node.op, ast.UAdd)): #UnaryOp
		# 	node.op = ast.USub()
		# elif(isinstance(node.op, ast.USub)): #UnaryOp
			node.op = ast.UAdd()

	def visit_BinOp(self, node): # +, -, *, %, floordiv/regular div?
		self.generic_visit(node)
		self.binop_count += 1
		if(self.binop_count == self.count_of_node_to_mutate):
			new_node = copy.deepcopy(node)
			self.swap_Op(new_node)
			return new_node
		else:
			return node
	# def visit_BoolOp(self, node):
	# 	if(self.num_mutations < self.total_mutations):
	# 		self.swap_Op(node)
	# 		return node
	# 	else:
	# 		return node
	# 	return node
	# def visit_UnaryOp(self, node):
	# 	if(self.num_mutations < self.total_mutations):
	# 		self.swap_Op(node)
	# 		return node
	# 	else:
	# 		return node



class StmtDeletion(ast.NodeTransformer): #between 0 and 1 mutations
	def __init__(self, count_of_node_to_mutate):
		self.assign_count = 0
		self.count_of_node_to_mutate = count_of_node_to_mutate

	def visit_Assign(self, node):
		# print('num stmts that should be deleted: ' + str(self.total_mutations))
		# print(self.num_mutations)
		self.generic_visit(node)
		self.assign_count += 1
		if(self.assign_count == self.count_of_node_to_mutate):
			return ast.Pass()
		else:
			return node
	# def visit_AnnAssign(self, node):
	# 	self.generic_visit(node)
	# 	if(self.num_mutations < self.total_mutations):
	# 		self.num_mutations += 1
	# 		return ast.Pass()
	# 	else:
	# 		return node
	# def visit_AugAssign(self, node):
	# 	self.generic_visit(node)
	# 	if(self.num_mutations < self.total_mutations):
	# 		self.num_mutations += 1
	# 		return ast.Pass()
	# 	else:
	# 		return node
	# def visit_Expr(self, node):
	# 	self.generic_visit(node)
	# 	if(self.num_mutations < self.total_mutations):
	# 		self.num_mutations += 1
	# 		return ast.Pass()
	# 	else:
	# 		return node

def main():
	file_name = sys.argv[1]
	num_mutants = sys.argv[2]
	print(file_name)
	file = open(file_name)
	file_string = file.read()
	file_tree = ast.parse(file_string) #read python source file into ast module
	random.seed(1) #seed random so its deterministically random



	#Walk through AST and collect operations of Compare, Assign, BinOps
	collector = Collector()
	collector.visit(file_tree)
	print("binop nodes to choose from: ", collector.binops_to_visit)
	random.shuffle(collector.binops_to_visit)
	print("compare nodes to choose from: ", collector.compare_to_visit)
	random.shuffle(collector.compare_to_visit)
	print("assign nodes to choose from: ", collector.assign_to_visit)
	random.shuffle(collector.assign_to_visit)

	for file_number in range(int(num_mutants)):
		to_mutate_binops = collector.binops_to_visit[:int(num_mutants)]
		to_mutate_compare = collector.compare_to_visit[:int(num_mutants)]
		to_mutate_assign = collector.assign_to_visit[:int(num_mutants)]
		file_tree = ast.parse(file_string) #read python source file into ast module
		mutator_type = random.randint(0,2)

		if mutator_type == 1:
			file_tree = SwapOperation(to_mutate_binops[file_number%len(to_mutate_binops)]).visit(file_tree) 
		elif mutator_type == 2:
			file_tree = RewriteNegateOperation(to_mutate_compare[file_number%len(to_mutate_compare)]).visit(file_tree)
		else:
			file_tree = StmtDeletion(to_mutate_assign[file_number%len(to_mutate_assign)]).visit(file_tree)
		f = open("{}.py".format(file_number), 'w+')
		mutated_python = astor.to_source(file_tree)
		f.write(mutated_python)




if __name__ == "__main__":
	main()

