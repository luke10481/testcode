import re

def add_route_decorator(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    func_pattern = re.compile(r'^def\s+(\w+)\(([^)]+)\):')

    for line in lines:
        match = func_pattern.match(line)
        if match:
            func_name = match.group(1)
            params = match.group(2).replace(" ", "").split(',')
            route = f'@app.route("/{func_name}/' + '/'.join([f'<{param}>' for param in params]) + '")\n'
            new_lines.append(route)
        new_lines.append(line)

    with open(file_path+'a', 'w') as file:
        file.writelines(new_lines)

# Example usage
file_path = 'testfile.py'
add_route_decorator(file_path)
