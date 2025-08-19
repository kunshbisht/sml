from pprint import pprint
import re
from dataclasses import dataclass
from typing import List, Optional, Union
import sys

# Token class
@dataclass
class Token:
	type: str
	value: str

# Regex patterns
TOKEN_SPEC = [
	("LBRACE", r"\{"),
	("RBRACE", r"\}"),
	("STRING", r'"([^"\\]|\\.)*"'),
	("JS_LITERAL", r"<\$([\s\S]*?)\$>"),
	("IDENT", r"[A-Za-z_]\w*"),
	("IMPORT", r"@\w+"),
	("NEWLINE", r"\n"),
	("WHITESPACE", r"[ \t]+"),
	("OTHER", r"."),
]

token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
token_re = re.compile(token_regex)

@dataclass
class Node:
	name: str
	children: Optional[List["Node"]] = None

# Lexer
def lex(code: str):
	tokens = []
	for match in token_re.finditer(code):
		kind = match.lastgroup
		value = match.group()
		if kind == "WHITESPACE":
			continue
		elif kind == "STRING":
			value = value[1:-1]
		elif kind == "IMPORT":
			value = value[1:]
		tokens.append(Token(type=kind, value=value))
	return tokens

class Parser:
	def __init__(self, tokens: list[Token]):
		self.tokens = tokens
		
	def eat(self, kind=''):
		if kind and not self.nextIs(kind):
			raise TypeError(f'Expected {kind} but got {self.peek().type} instead')
		return self.tokens.pop(0)
	
	def skip(self, kind='NEWLINE'):
		while self.nextIs(kind):
			self.eat(kind)
	
	def peek(self, index=0):
		return self.tokens[index]
	
	def nextIs(self, kind: str, index = 0):
		return self.peek(index).type == kind

	def parse(self):
		return self.parse_el()

	def parse_el(self) -> Node:
		name = self.eat('IDENT').value
		children = self.parse_children()
		return Node(name, children)

	def parse_import(self):
		key = self.eat('IMPORT').value
		return f'<script src="https://cdn.jsdelivr.net/gh/kunshbisht/sml/{key}.js"></script>'

	def parse_children(self):
		if self.nextIs('LBRACE'): return self.parse_block()
		elif self.nextIs('NEWLINE'):
			self.skip()
			return []
		return [self.parse_child()]
	
	def parse_child(self):
		if self.nextIs('IDENT'): return self.parse_el()
		elif self.nextIs('STRING'): return self.parse_string()
		elif self.nextIs('IMPORT'): return self.parse_import()
		raise TypeError(f'Unexpected type {self.peek().type}')
	
	def parse_string(self):
		return self.eat('STRING').value.replace('\\"', '"')
	
	def parse_block(self):
		result = []
		self.eat('LBRACE')
		self.skip()
		while not self.nextIs('RBRACE'):
			result.append(self.parse_child())
			self.skip()
		self.eat('RBRACE')
		return result

def SML2HTML(tree: Union[str, Node], indent: int = 0) -> str:
	totalIndent = "\t" * indent
	# Strings are just leaf nodes
	if isinstance(tree, str):
		return '\n'.join([totalIndent + line for line in tree.split('\n')]) + "\n"

	# Otherwise it's a Node
	inner = "".join([SML2HTML(child, indent + 1) for child in (tree.children or [])])

	# Opening and closing tag
	opening = totalIndent + f"<{tree.name}>\n"
	closing = totalIndent + f"</{tree.name}>\n"

	return opening + inner + closing

code = open(sys.argv[1]).read()
parser = Parser(lex(code))
ast = parser.parse()
output = SML2HTML(ast)
open('index.html', 'w').write(output)