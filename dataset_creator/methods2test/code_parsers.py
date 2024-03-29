"""Parser for parsing a Java code file.

Adapted from Methods2Test (https://arxiv.org/abs/2203.12776).
"""
from tree_sitter import Language, Parser
from typing import List, Dict, Any, Set, Optional

class CodeParser():
	
	def __init__(self, grammar_file, language):
		JAVA_LANGUAGE = Language(grammar_file, language)
		self.parser = Parser()
		self.parser.set_language(JAVA_LANGUAGE)


	def parse_file(self, file):
		"""
		Parses a java file and extract metadata of all the classes and methods defined
		"""

		#Build Tree
		with open(file, 'r') as content_file:
			try: 
				content = content_file.read()
				self.content = content
			except:
				return list()
		tree = self.parser.parse(bytes(content, "utf8"))
		packages = [node for node in tree.root_node.children
			if node.type == 'package_declaration']
		package = packages[0]
		package_identifier_nodes = [node for node in package.children
			if node.type == 'scoped_identifier']
		package_identifier_node = package_identifier_nodes[0]
		package_identifier = (CodeParser
			.match_from_span(package_identifier_node, content).strip())
		classes = (node for node in tree.root_node.children if node.type == 'class_declaration')
		#print(tree.root_node.sexp())
		
		#Parsed Classes
		parsed_classes = list()

		#Classes
		for _class in classes:

			#Class metadata
			class_identifier = self.match_from_span([child for child in _class.children if child.type == 'identifier'][0], content).strip()
			class_metadata = self.get_class_metadata(_class, content)

			methods = list()

			#Parse methods
			for child in (child for child in _class.children if child.type == 'class_body'):
				for _, node in enumerate(child.children):
					if node.type == 'method_declaration' or node.type == 'constructor_declaration':	
						
						#Read Method metadata
						method_metadata = CodeParser.get_function_metadata(class_identifier, node, content)
						methods.append(method_metadata)

			class_metadata['package'] = package_identifier
			class_metadata['methods'] = methods
			parsed_classes.append(class_metadata)

		return parsed_classes



	@staticmethod
	def get_class_metadata(class_node, blob: str):
		"""
		Extract class-level metadata 
		"""
		metadata = {
			'package': '',
			'identifier': '',
			'superclass': '',
			'interfaces': '',
			'line_start': '',
			'col_start': '',
			'line_end': '',
			'col_end': '',
			'fields': '',
			'argument_list': '',
			'methods':'',
		}

		#Superclass
		superclass = class_node.child_by_field_name('superclass')
		if superclass:
			metadata['superclass'] = CodeParser.match_from_span(superclass, blob)
		
		#Interfaces
		interfaces = class_node.child_by_field_name('interfaces')
		if interfaces:
			metadata['interfaces'] = CodeParser.match_from_span(interfaces, blob)
		
		#Fields
		fields = CodeParser.get_class_fields(class_node, blob)
		metadata['fields'] = fields

		#Identifier and Arguments
		is_header = False
		for n in class_node.children:
			if is_header:
				if n.type == 'identifier':
					metadata['identifier'] = CodeParser.match_from_span(n, blob).strip('(:')
				elif n.type == 'argument_list':
					metadata['argument_list'] = CodeParser.match_from_span(n, blob)
			if n.type == 'class':
				is_header = True
			elif n.type == ':':
				break

		# Start and end points of the class
		metadata['line_start'] = class_node.start_point[0]
		metadata['col_start'] = class_node.start_point[1]
		metadata['line_end'] = class_node.end_point[0]
		metadata['col_end'] = class_node.end_point[1]

		return metadata



	@staticmethod
	def get_class_fields(class_node, blob: str):
		"""
		Extract metadata for all the fields defined in the class
		"""
		
		body_node = class_node.child_by_field_name("body")
		fields = []
		
		for f in CodeParser.children_of_type(body_node, "field_declaration"):
			field_dict = {}

			#Complete field
			field_dict["original_string"] = CodeParser.match_from_span(f, blob)

			#Modifier
			modifiers_node_list = CodeParser.children_of_type(f, "modifiers")
			if len(modifiers_node_list) > 0:
				modifiers_node = modifiers_node_list[0]
				field_dict["modifier"] = CodeParser.match_from_span(modifiers_node, blob)
			else:
				field_dict["modifier"] = ""

			#Type
			type_node = f.child_by_field_name("type")
			field_dict["type"] = CodeParser.match_from_span(type_node, blob)

			#Declarator
			declarator_node = f.child_by_field_name("declarator")
			field_dict["declarator"] = CodeParser.match_from_span(declarator_node, blob)
			
			#Var name
			var_node = declarator_node.child_by_field_name("name")
			field_dict["var_name"] = CodeParser.match_from_span(var_node, blob)

			fields.append(field_dict)

		return fields



	@staticmethod
	def get_function_metadata(class_identifier, function_node, blob: str):
		"""
		Extract method-level metadata 
		"""		
		metadata = {
			'identifier': '',
			'parameters': '',
			'modifiers': '',
			'return' : '',
			'line_start': '',
			'col_start': '',
			'line_end': '',
			'col_end': '',
			'body': '',
			'class': '',
			'signature': '',
			'full_signature': '',
			'class_method_signature': '',
			'testcase': '',
			'constructor': '',
		}

		# Parameters
		declarators = []
		CodeParser.traverse_type(function_node, declarators, '{}_declaration'.format(function_node.type.split('_')[0]))
		parameters = []
		for n in declarators[0].children:
			if n.type == 'identifier':
				metadata['identifier'] = CodeParser.match_from_span(n, blob).strip('(')
			elif n.type == 'formal_parameters':
				parameters.append(CodeParser.match_from_span(n, blob))
		metadata['parameters'] = ' '.join(parameters)

		#Body
		metadata['line_start'] = function_node.start_point[0]
		metadata['col_start'] = function_node.start_point[1]
		metadata['line_end'] = function_node.end_point[0]
		metadata['col_end'] = function_node.end_point[1]
		metadata['body'] = CodeParser.match_from_span(function_node, blob)
		metadata['class'] = class_identifier

		#Constructor
		metadata['constructor'] = False
		if "constructor" in function_node.type:
			metadata['constructor'] = True

		#Test Case
		modifiers_node_list = CodeParser.children_of_type(function_node, "modifiers")
		metadata['testcase'] = False
		for m in modifiers_node_list:
			modifier = CodeParser.match_from_span(m, blob)
			if '@Test' in modifier:
				metadata['testcase'] = True

		#Method Invocations
		invocation = []
		method_invocations = list()
		CodeParser.traverse_type(function_node, invocation, '{}_invocation'.format(function_node.type.split('_')[0]))
		for inv in invocation:
			name = inv.child_by_field_name('name')
			method_invocation = CodeParser.match_from_span(name, blob)
			method_invocations.append(method_invocation)
		metadata['invocations'] = method_invocations

		#Modifiers and Return Value
		for child in function_node.children:
			if child.type == "modifiers":
				metadata['modifiers']  = ' '.join(CodeParser.match_from_span(child, blob).split())
			if("type" in child.type):
				metadata['return'] = CodeParser.match_from_span(child, blob)
		
		#Signature
		metadata['signature'] = '{} {}{}'.format(metadata['return'], metadata['identifier'], metadata['parameters'])
		metadata['full_signature'] = '{} {} {}{}'.format(metadata['modifiers'], metadata['return'], metadata['identifier'], metadata['parameters'])
		metadata['class_method_signature'] = '{}.{}{}'.format(class_identifier, metadata['identifier'], metadata['parameters'])

		return metadata


	def get_method_names(self, file):
		"""
		Extract the list of method names defined in a file
		"""

		#Build Tree
		with open(file, 'r') as content_file: 
			content = content_file.read()
			self.content = content
		tree = self.parser.parse(bytes(content, "utf8"))
		classes = (node for node in tree.root_node.children if node.type == 'class_declaration')

		#Method names
		method_names = list()

		#Class
		for _class in classes:		
			#Iterate methods
			for child in (child for child in _class.children if child.type == 'class_body'):
				for _, node in enumerate(child.children):
					if node.type == 'method_declaration':
						if not CodeParser.is_method_body_empty(node):
							
							#Method Name
							method_name = CodeParser.get_function_name(node, content)
							method_names.append(method_name)

		return method_names


	@staticmethod
	def get_function_name(function_node, blob: str):
		"""
		Extract method name
		"""
		declarators = []
		CodeParser.traverse_type(function_node, declarators, '{}_declaration'.format(function_node.type.split('_')[0]))
		for n in declarators[0].children:
			if n.type == 'identifier':
				return CodeParser.match_from_span(n, blob).strip('(')


	@staticmethod
	def match_from_span(node, blob: str) -> str:
		"""
		Extract the source code associated with a node of the tree
		"""
		line_start = node.start_point[0]
		line_end = node.end_point[0]
		char_start = node.start_point[1]
		char_end = node.end_point[1]
		lines = blob.split('\n')
		if line_start != line_end:
			return '\n'.join([lines[line_start][char_start:]] + lines[line_start+1:line_end] + [lines[line_end][:char_end]])
		else:
			return lines[line_start][char_start:char_end]


	@staticmethod
	def traverse_type(node, results: List, kind: str) -> None:
		"""
		Traverses nodes of given type and save in results
		"""
		if node.type == kind:
			results.append(node)
		if not node.children:
			return
		for n in node.children:
			CodeParser.traverse_type(n, results, kind)


	@staticmethod
	def is_method_body_empty(node):
		"""
		Check if the body of a method is empty
		"""
		for c in node.children:
			if c.type in {'method_body', 'constructor_body'}:
				if c.start_point[0] == c.end_point[0]:
					return True

	
	@staticmethod
	def children_of_type(node, types):
		"""
		Return children of node of type belonging to types

		Parameters
		----------
		node : tree_sitter.Node
			node whose children are to be searched
		types : str/tuple
			single or tuple of node types to filter

		Return
		------
		result : list[Node]
			list of nodes of type in types
		"""
		if isinstance(types, str):
			return CodeParser.children_of_type(node, (types,))
		return [child for child in node.children if child.type in types]
