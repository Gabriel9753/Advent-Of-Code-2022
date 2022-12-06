import os
with open(f'python_scripts/template.txt', 'r') as f:
    template = f.read()
for i in range(1, 26):
    # if os.path.exists(f"python_scripts/day_{i}.py"):
    #     print(f"src/scripts/day_{i}.py already exists!")
    #     continue
    with open(f'python_scripts/day_{i}.txt', 'w') as fp:
        pass
    with open(f'python_scripts/day_{i}.py', 'w') as fp:
        fp.write(template)
