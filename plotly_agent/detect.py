import ast


class MaliciousCodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.malicious = False

    def visit_Call(self, node):
        # Check for calls to dangerous functions
        dangerous_functions = {"exec", "eval", "compile", "getattr", "setattr", "delattr", "globals", "locals"}
        if isinstance(node.func, ast.Name) and node.func.id in dangerous_functions:
            print(f"Malicious code detected: {node.func.id}() on line {node.lineno}")
            self.malicious = True
        self.generic_visit(node)

    def visit_Import(self, node):
        # Warn about potentially dangerous imports
        for alias in node.names:
            if alias.name in {"os", "sys", "subprocess", "importlib"}:
                print(f"Potentially dangerous import detected: {alias.name} on line {node.lineno}")
                self.malicious = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Warn about imports from specific dangerous modules
        if node.module in {"os", "sys", "subprocess", "importlib"}:
            print(f"Potentially dangerous import detected: {node.module} on line {node.lineno}")
            self.malicious = True
        self.generic_visit(node)

    def visit_Str(self, node):
        # Detect the use of dangerous strings
        if any(keyword in node.s for keyword in {"exec", "eval", "compile"}):
            print(f"Suspicious string detected: '{node.s}' on line {node.lineno}")
            self.malicious = True
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Detect the use of attributes like exec or eval
        if isinstance(node.value, ast.Name) and node.attr in {"exec", "eval", "compile"}:
            print(f"Potential dynamic execution via {node.attr} detected on line {node.lineno}")
            self.malicious = True
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Detect dangerous subclassing
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id in {"type"}:
                print(f"Subclassing detected with base '{base.id}' on line {node.lineno}")
                self.malicious = True
        self.generic_visit(node)


def check_malicious_code(code):
    tree = ast.parse(code)
    visitor = MaliciousCodeVisitor()
    visitor.visit(tree)
    return visitor.malicious