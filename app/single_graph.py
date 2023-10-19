
import os
import ast
from collections import defaultdict

# Function to extract import statements from a Python file using AST
def extract_imports(file_path):
    with open(file_path, 'r') as f:
        file_content = f.read()

    # Parse the file content into an AST
    tree = ast.parse(file_content)

    # Extract import statements
    import_statements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                import_statements.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for n in node.names:
                if module:
                    import_statements.append(f"{module}.{n.name}")
                else:
                    import_statements.append(n.name)

    return import_statements

# Function to add an edge to the graph
def add_edge(graph, u, v):
    graph[u].append(v)

# Function to perform topological sort
def topological_sort(graph, node, visited, stack):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            topological_sort(graph, neighbor, visited, stack)
    stack.append(node)

# Path to the root directory of the Python project
project_root = "/Users/jacob.akerson/_Dev/jacobgoldenart/ghostLLM/src/"


# List of folders or files to ignore
ignore_list = ["utils", "singlefile.py"]

# Filter function to check if a file or folder should be ignored
def should_ignore(path):
    for ignore_item in ignore_list:
        if ignore_item in path.split('/'):
            return True
    return False

# List Python files in the project directory, skipping those in the ignore list
python_files = [os.path.join(root, file) for root, dirs, files in os.walk(project_root) for file in files if file.endswith('.py') and '/.' not in os.path.join(root, file) and not should_ignore(os.path.join(root, file))]

# Analyze each Python file and collect its import statements
file_imports = {}
for file_path in python_files:
    file_imports[file_path] = extract_imports(file_path)


# Debug: Print the import statements detected for each file
print("Debug: Import statements detected for each file")
for file_path, imports in file_imports.items():
    print(f"{file_path}: {imports}")

print("Debug: Generated file paths for internal imports")
for file_path, imports in file_imports.items():
    for imp in imports:
        import_path = imp.split('.')
        separator = "" if project_root.endswith("/") else "/"
        import_file = os.path.join(project_root, '/'.join(import_path[:-1]), f"{import_path[-1]}.py")
        print(f"{imp} -> {import_file}")

# Initialize dependency graph
dependency_graph = defaultdict(list)

# Populate the dependency graph
for file_path, imports in file_imports.items():
    for imp in imports:
        import_path = imp.split('.')
        import_file = os.path.join(project_root, '/'.join(import_path[:-1]), f"{import_path[-1]}.py")
        if import_file in python_files:
            add_edge(dependency_graph, import_file, file_path)

# Perform topological sort to determine the correct order of files
visited = set()
stack = []
for file_path in python_files:
    if file_path not in visited:
        topological_sort(dependency_graph, file_path, visited, stack)

# The stack now contains the files in the correct order
correct_order_files = stack[::-1]

# Function to combine Python files into a single file
def combine_files(file_paths, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for file_path in file_paths:
            with open(file_path, 'r') as input_file:
                file_content = input_file.read()

            file_name = os.path.basename(file_path)
            output_file.write(f"\n# === File: {file_name} ===\n")

            output_file.write(file_content)

# Combine the files in the correct order into a single file
output_file_path = "/Users/jacob.akerson/_Dev/jacobgoldenart/ghostLLM/utils/single.py"
combine_files(correct_order_files, output_file_path)

# Function to generate a DOT file for Graphviz to visualize the dependency graph
def generate_dot_file(graph, dot_file_path):
    with open(dot_file_path, 'w') as f:
        f.write("digraph G {\n")
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                f.write(f'    "{os.path.basename(node)}" -> "{os.path.basename(neighbor)}";\n')
        f.write("}\n")

# Generate the DOT file
dot_file_path = (
    "/Users/jacob.akerson/_Dev/jacobgoldenart/ghostLLM/utils/dependency_graph.dot"
)

print(dependency_graph)
generate_dot_file(dependency_graph, dot_file_path)
