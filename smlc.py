import sys
from parser import lex, Parser, SML2HTML
import importlib.resources

def compile_sml(input_file, output_file):
    # Parse SML
    code = open(input_file).read()
    tokens = lex(code)
    parser = Parser(tokens)
    ast = parser.parse()
    html = SML2HTML(ast)

    # Write final HTML
    with open(output_file, "w") as f:
        f.write(html)

    print(f"Compiled {input_file} → {output_file}")

def main():
    if len(sys.argv) < 4 or sys.argv[2] != "-o":
        print("Usage: smlc input.sml -o output.html")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[3]
    compile_sml(input_file, output_file)
