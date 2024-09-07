import os
import subprocess
from colorama import Fore, Style, init
import time

# Initialize colorama for Windows support
init(autoreset=True)


def print_welcome_message():
    welcome_message = """
    {0}==========================================
    ||                                       ||
    ||   {1}Project Initializer CLI Tool{0}         ||
    ||                                       ||
    ==========================================
    """.format(Fore.CYAN, Fore.YELLOW)
    print(welcome_message)


def print_progress(message):
    print(f"{Fore.GREEN}✔ {message}")


def create_common_files(project_name, project_dir, language):
    # Create a common .env, language-specific .gitignore, Makefile, Dockerfile, and .dockerignore
    dockerignore = """
# Ignore unnecessary files in Docker builds
.git
*.pyc
__pycache__
node_modules/
tests/
.env
    """

    env_file = """
# Environment variables
DEBUG=True
PORT=8080
    """

    with open(os.path.join(project_dir, ".env"), "w") as f:
        f.write(env_file)

    with open(os.path.join(project_dir, ".dockerignore"), "w") as f:
        f.write(dockerignore)

    print_progress(".env and .dockerignore files created.")

    # Language-specific file creation
    if language == "python":
        create_python_files(project_name, project_dir)
    elif language == "golang":
        create_golang_files(project_name, project_dir)
    elif language == "typescript":
        create_typescript_files(project_name, project_dir)
    elif language == "rust":
        create_rust_files(project_name, project_dir)


def create_python_files(project_name, project_dir):
    gitignore = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*.so

# Virtual environment
venv/
.env
    """

    makefile = f"""
# Makefile for Python project

.PHONY: all build run test docker-build docker-run clean

all: run

run:
\t@echo "Running {project_name}..."
\tdocker-compose up --build

test:
\t@echo "Running tests..."
\tpytest

docker-build:
\tdocker build -t {project_name} .

docker-run:
\tdocker run -it --rm -p 8080:8080 --env-file .env {project_name}

clean:
\t@echo "Cleaning project..."
\trm -rf __pycache__ .pytest_cache
    """

    dockerfile = f"""
# Dockerfile for Python project using Alpine

FROM python:alpine

WORKDIR /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port for the service
EXPOSE 8080

CMD ["python3", "app/__init__.py"]
    """

    with open(os.path.join(project_dir, ".gitignore"), "w") as f:
        f.write(gitignore)

    with open(os.path.join(project_dir, "Makefile"), "w") as f:
        f.write(makefile)

    with open(os.path.join(project_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile)

    print_progress("Python-specific files (.gitignore, Makefile, Dockerfile) created.")


def create_golang_files(project_name, project_dir):
    gitignore = """
# Binaries for programs and plugins
*.exe
*.dll
*.so
*.dylib
bin/
vendor/
.env
    """

    makefile = f"""
# Makefile for Go project

.PHONY: all build run test docker-build docker-run clean

all: build

build:
\t@echo "Building {project_name}..."
\tdocker build -t {project_name} .

run:
\t@echo "Running {project_name}..."
\tdocker-compose up --build

test:
\t@echo "Running tests..."
\tgo test ./...

docker-build:
\tdocker build -t {project_name} .

docker-run:
\tdocker run -it --rm -p 8080:8080 --env-file .env {project_name}

clean:
\t@echo "Cleaning project..."
\tgo clean
    """

    dockerfile = f"""
# Dockerfile for Go project using Alpine

FROM golang:alpine

WORKDIR /app
COPY . .

# Download dependencies
RUN go mod download

# Build the Go app
RUN go build -o main ./cmd/{project_name}/main.go

# Expose a port for the service
EXPOSE 8080

CMD ["./main"]
    """

    with open(os.path.join(project_dir, ".gitignore"), "w") as f:
        f.write(gitignore)

    with open(os.path.join(project_dir, "Makefile"), "w") as f:
        f.write(makefile)

    with open(os.path.join(project_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile)

    print_progress("Golang-specific files (.gitignore, Makefile, Dockerfile) created.")


def create_typescript_files(project_name, project_dir):
    gitignore = """
# Ignore node_modules and log files
node_modules/
dist/
npm-debug.log
.env
    """

    makefile = f"""
# Makefile for TypeScript project

.PHONY: all build run test docker-build docker-run clean

all: build

build:
\t@echo "Building {project_name}..."
\tdocker build -t {project_name} .

run:
\t@echo "Running {project_name}..."
\tdocker-compose up --build

test:
\t@echo "Running tests..."
\tnpm test

docker-build:
\tdocker build -t {project_name} .

docker-run:
\tdocker run -it --rm -p 8080:8080 --env-file .env {project_name}

clean:
\t@echo "Cleaning project..."
\trm -rf node_modules dist
    """

    dockerfile = f"""
FROM node:alpine

WORKDIR /app
COPY . .

# Install dependencies
RUN npm install

# Build the TypeScript app
RUN npm run build

# Expose a port for the service
EXPOSE 8080

CMD ["npm", "start"]
    """

    with open(os.path.join(project_dir, ".gitignore"), "w") as f:
        f.write(gitignore)

    with open(os.path.join(project_dir, "Makefile"), "w") as f:
        f.write(makefile)

    with open(os.path.join(project_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile)

    print_progress("TypeScript-specific files (.gitignore, Makefile, Dockerfile) created.")


def create_rust_files(project_name, project_dir):
    gitignore = """
# Cargo
/target/
**/*.rs.bk
.env
    """

    makefile = f"""
# Makefile for Rust project

.PHONY: all build run test docker-build docker-run clean

all: build

build:
\t@echo "Building {project_name}..."
\tdocker build -t {project_name} .

run:
\t@echo "Running {project_name}..."
\tdocker-compose up --build

test:
\t@echo "Running tests..."
\tcargo test

docker-build:
\tdocker build -t {project_name} .

docker-run:
\tdocker run -it --rm -p 8080:8080 --env-file .env {project_name}

clean:
\t@echo "Cleaning project..."
\tcargo clean
    """

    dockerfile = f"""
# Dockerfile for Rust project using Alpine

FROM rust:alpine

WORKDIR /app
COPY . .

# Build the Rust app
RUN cargo build --release

# Expose a port for the service
EXPOSE 8080

CMD ["./target/release/{project_name}"]
    """

    with open(os.path.join(project_dir, ".gitignore"), "w") as f:
        f.write(gitignore)

    with open(os.path.join(project_dir, "Makefile"), "w") as f:
        f.write(makefile)

    with open(os.path.join(project_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile)

    print_progress("Rust-specific files (.gitignore, Makefile, Dockerfile) created.")


def golang_structure(project_name, project_dir):
    structure = f"""#!/bin/bash
mkdir -p {project_dir}/{{cmd/{project_name},internal,api,configs,pkg,web,docs,scripts}}
mkdir -p {project_dir}/{{internal/app,internal/config,internal/domain,internal/repository,internal/usecase}}
touch {project_dir}/{{README.md,go.mod,go.sum}}
touch {project_dir}/{{cmd/{project_name}/main.go,api/swagger.yml,configs/config.yaml,docs/README.md,scripts/bootstrap.sh}}

cat <<EOF > {project_dir}/cmd/{project_name}/main.go
package main

func main() {{
    // Your application entry point
}}
EOF
"""
    return structure


def typescript_structure(project_name, project_dir):
    structure = f"""#!/bin/bash
mkdir -p {project_dir}/{{src/{{controllers,routes,models,services,utils}},config,tests,public,docs,scripts}}
touch {project_dir}/{{README.md,tsconfig.json,package.json}}
touch {project_dir}/src/index.ts
touch {project_dir}/config/default.json
touch {project_dir}/tests/index.test.ts
touch {project_dir}/scripts/start.sh

cat <<EOF > {project_dir}/src/index.ts
import express from 'express';

const app = express();

app.get('/', (req, res) => res.send('Hello World'));

app.listen(3000, () => console.log('Server running on port 3000'));
EOF
"""
    return structure


def rust_structure(project_name, project_dir):
    structure = f"""#!/bin/bash
cargo new --bin {project_name}
cd {project_dir}
mkdir -p src/{{config,controllers,models,repositories,services,utils,tests}}
touch src/{{main.rs,config/mod.rs,controllers/mod.rs,models/mod.rs,repositories/mod.rs,services/mod.rs,utils/mod.rs}}

cat <<EOF > src/main.rs
fn main() {{
    println!("Hello, Rust!");
}}
EOF
"""
    return structure


def python_structure(project_name, project_dir):
    structure = f"""#!/bin/bash
mkdir -p {project_dir}/{{app/{{api,core,models,repositories,services,utils}},config,tests,docs,scripts}}
touch {project_dir}/{{README.md,requirements.txt}}
touch {project_dir}/app/__init__.py
touch {project_dir}/app/api/__init__.py
touch {project_dir}/app/core/__init__.py
touch {project_dir}/app/models/__init__.py
touch {project_dir}/app/repositories/__init__.py
touch {project_dir}/app/services/__init__.py
touch {project_dir}/app/utils/__init__.py
touch {project_dir}/config/config.yaml
touch {project_dir}/tests/test_app.py
touch {project_dir}/scripts/start.sh

cat <<EOF > {project_dir}/app/__init__.py
# Application module initialization
EOF

cat <<EOF > {project_dir}/tests/test_app.py
def test_example():
    assert 1 + 1 == 2
EOF
"""
    return structure


def generate_project(language, project_name, project_dir):
    structures = {
        'golang': golang_structure,
        'typescript': typescript_structure,
        'rust': rust_structure,
        'python': python_structure
    }
    if language not in structures:
        print(f"{Fore.RED}Error: Unsupported language: {language}")
        return

    # Create project structure
    script_content = structures[language](project_name, project_dir)
    script_path = f"./generate_{project_name}.sh"

    with open(script_path, 'w') as script_file:
        script_file.write(script_content)

    print(f"{Fore.YELLOW}Generating project structure...")

    # Simulate progress
    time.sleep(1)
    subprocess.run(["chmod", "+x", script_path])
    subprocess.run([script_path])
    os.remove(script_path)

    # Create common files
    create_common_files(project_name, project_dir, language)

    print_progress(f"{language.capitalize()} project '{project_name}' generated successfully.")


def validate_language(language):
    supported_languages = ['golang', 'typescript', 'rust', 'python']
    if language not in supported_languages:
        print(
            f"{Fore.RED}Error: Unsupported language '{language}'. Supported languages are: {', '.join(supported_languages)}")
        return False
    return True


def validate_project_name(project_name):
    if not project_name or not project_name.isidentifier():
        print(f"{Fore.RED}Error: Invalid project name '{project_name}'.")
        return False
    return True


def validate_project_directory(directory):
    if not os.path.isdir(directory):
        try:
            os.makedirs(directory)
            print_progress(f"Directory '{directory}' created.")
        except OSError:
            print(f"{Fore.RED}Error: Unable to create directory '{directory}'.")
            return False
    return True


def main():
    print_welcome_message()

    print(f"{Fore.BLUE}Supported languages: golang, typescript, rust, python")

    # Input language and validate
    language = input(f"{Fore.YELLOW}Enter the programming language: ").strip().lower()
    if not validate_language(language):
        return

    # Input project name and validate
    project_name = input(f"{Fore.YELLOW}Enter your project name: ").strip()
    if not validate_project_name(project_name):
        return

    # Input project directory and validate
    project_dir = input(
        f"{Fore.YELLOW}Enter the directory where the project should be created (default is current directory): ").strip()
    if not project_dir:
        project_dir = os.getcwd()  # Use the current directory if not specified
    else:
        project_dir = os.path.join(project_dir, project_name)

    if not validate_project_directory(project_dir):
        return

    # Generate project structure
    generate_project(language, project_name, project_dir)


if __name__ == "__main__":
    main()
