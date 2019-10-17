import ast
import astor
import sys

# To Do's:
# 1. Probabilities
# 2. What's next 

class RewriteNegateOperation(ast.NodeTransformer): #subclass of NodeTransformer 
	def NegateOperation(self, node):
		for op in range(len(node.ops)):
			if(isinstance(node.ops[op], ast.Eq)):
				node.ops[op] = ast.NotEq()
			elif (isinstance(node.ops[op], ast.NotEq)):
				node.ops[op] = ast.Eq()
			elif (isinstance(node.ops[op], ast.Lt)):
				node.ops[op] = ast.Gt()
			elif (isinstance(node.ops[op], ast.Gt)):
				node.ops[op] = ast.Lt()
			elif (isinstance(node.ops[op], ast.LtE)):
				node.ops[op] = ast.GtE()
			elif (isinstance(node.ops[op], ast.GtE)):
				node.ops[op] = ast.LtE()
			elif (isinstance(node.ops[op], ast.Is)):
				node.ops[op] = ast.IsNot()
			elif (isinstance(node.ops[op], ast.IsNot)):
				node.ops[op] = ast.Is()
			elif (isinstance(node.ops[op], ast.In)):
				node.ops[op] = ast.NotIn()
			elif (isinstance(node.ops[op], ast.NotIn)):
				node.ops[op] = ast.In() 

	def visit_Compare(self, node):
		#call generic visit first
		self.generic_visit(node)
		print(node.ops)
		for op in range(len(node.ops)):
			print(type(node.ops[op]))
			self.NegateOperation(node)
			print(type(node.ops[op]))
		print(node.ops)
		return node

class SwapOperation(ast.NodeTransformer):
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
		elif(isinstance(node.op, ast.And)): #BoolOp
			node.op = ast.Or()
		elif(isinstance(node.op, ast.Or)): #BoolOp
			node.op = ast.And()
		elif(isinstance(node.op, ast.UAdd)): #UnaryOp
			node.op = ast.USub()
		elif(isinstance(node.op, ast.USub)): #UnaryOp
			node.op = ast.UAdd()

	def visit_BinOp(self, node): # +, -, *, %, floordiv/regular div?
		self.generic_visit(node)
		self.swap_Op(node)
		return node
	def visit_BoolOp(self, node):
		self.generic_visit(node)
		self.swap_Op(node)
		return node
	def visit_UnaryOp(self, node):
		self.generic_visit(node)
		self.swap_Op(node)
		return node

class StmtDeletion(ast.NodeTransformer):
	def visit_Assign(self, node):
		self.generic_visit(node)
		return ast.Pass()
	def visit_AnnAssign(self, node):
		self.generic_visit(node)
		return ast.Pass()
	def visit_AugAssign(self, node):
		self.generic_visit(node)
		return ast.Pass()
	def visit_Expr(self, node):
		self.generic_visit(node)
		return ast.Pass()

def main():
	file_name = sys.argv[1]
	num_mutants = sys.argv[2]
	print(file_name)
	file = open(file_name)
	file_string = file.read()

	for file_number in range(int(num_mutants)):
		file_tree = ast.parse(file_string) #read python source file into ast module

		#print(astor.dump_tree(file_tree))
		file_tree = RewriteNegateOperation().visit(file_tree) #need to transform child nodes or call generic_visit(method) for node first
		file_tree = SwapOperation().visit(file_tree)
		file_tree = StmtDeletion().visit(file_tree)
		ast.fix_missing_locations(file_tree)
		#print(astor.to_source(file_tree))

		mutated_python = astor.to_source(file_tree)

		print(file_number)
		f = open("{}.py".format(file_number), 'w+')
		#exec(compile(astor.to_source(file_tree), filename="<ast>", mode="exec"))




if __name__ == "__main__":
	main()

