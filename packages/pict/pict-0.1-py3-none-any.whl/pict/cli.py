import os
import argparse
from colorama import Fore, init

# Initialize colorama for colored output in terminal
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
    # Create common files: .env, Dockerfile, Makefile, .dockerignore
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

    if language == "python":
        create_python_files(project_name, project_dir)
    elif language == "golang":
        create_golang_files(project_name, project_dir)
    elif language == "typescript":
        create_typescript_files(project_name, project_dir)
    elif language == "rust":
        create_rust_files(project_name, project_dir)


# Function to create folder structure and files for Python projects
def create_python_files(project_name, project_dir):
    folders = [
        "app/api", "app/core", "app/models", "app/repositories", "app/services", "app/utils",
        "config", "tests", "docs", "scripts"
    ]
    files = {
        "README.md": "",
        "requirements.txt": "",
        "app/__init__.py": "# Application module initialization",
        "app/api/__init__.py": "",
        "app/core/__init__.py": "",
        "app/models/__init__.py": "",
        "app/repositories/__init__.py": "",
        "app/services/__init__.py": "",
        "app/utils/__init__.py": "",
        "config/config.yaml": "",
        "tests/test_app.py": "def test_example():\n    assert 1 + 1 == 2",
        "scripts/start.sh": "#!/bin/bash\n# Start script"
    }

    for folder in folders:
        os.makedirs(os.path.join(project_dir, folder), exist_ok=True)

    for file, content in files.items():
        with open(os.path.join(project_dir, file), "w") as f:
            f.write(content)

    print_progress("Python project structure and files created.")


# Function to create folder structure and files for Golang projects
def create_golang_files(project_name, project_dir):
    folders = [
        f"cmd/{project_name}", "internal/app", "internal/config", "internal/domain", "internal/repository",
        "internal/usecase",
        "api", "configs", "pkg", "web", "docs", "scripts"
    ]
    files = {
        "README.md": "",
        f"cmd/{project_name}/main.go": f"package main\n\nfunc main() {{\n    // Your application entry point\n}}",
        "go.mod": f"module {project_name}\n\ngo 1.18\n",
        "api/swagger.yml": "",
        "configs/config.yaml": "",
        "docs/README.md": "",
        "scripts/bootstrap.sh": "#!/bin/bash\n# Bootstrap script"
    }

    for folder in folders:
        os.makedirs(os.path.join(project_dir, folder), exist_ok=True)

    for file, content in files.items():
        with open(os.path.join(project_dir, file), "w") as f:
            f.write(content)

    print_progress("Golang project structure and files created.")


# Function to create folder structure and files for TypeScript projects
def create_typescript_files(project_name, project_dir):
    folders = [
        "src/controllers", "src/routes", "src/models", "src/services", "src/utils",
        "config", "tests", "public", "docs", "scripts"
    ]
    files = {
        "README.md": "",
        "tsconfig.json": "{}",
        "package.json": "{}",
        "src/index.ts": """
import express from 'express';

const app = express();

app.get('/', (req, res) => res.send('Hello World'));

app.listen(3000, () => console.log('Server running on port 3000'));
""",
        "config/default.json": "",
        "tests/index.test.ts": "",
        "scripts/start.sh": "#!/bin/bash\n# Start script"
    }

    for folder in folders:
        os.makedirs(os.path.join(project_dir, folder), exist_ok=True)

    for file, content in files.items():
        with open(os.path.join(project_dir, file), "w") as f:
            f.write(content)

    print_progress("TypeScript project structure and files created.")


# Function to create folder structure and files for Rust projects
def create_rust_files(project_name, project_dir):
    os.makedirs(project_dir, exist_ok=True)
    os.system(f"cargo init {project_dir}")

    # Additional directories and files
    folders = ["src/config", "src/controllers", "src/models", "src/repositories", "src/services", "src/utils", "tests"]
    for folder in folders:
        os.makedirs(os.path.join(project_dir, folder), exist_ok=True)

    with open(os.path.join(project_dir, "src/main.rs"), "w") as f:
        f.write('fn main() {\n    println!("Hello, Rust!");\n}')

    print_progress("Rust project structure and files created.")


# Function to generate project structure based on language
def generate_project(language, project_name, project_dir):
    structures = {
        'golang': create_golang_files,
        'typescript': create_typescript_files,
        'rust': create_rust_files,
        'python': create_python_files
    }

    if language not in structures:
        print(f"{Fore.RED}Error: Unsupported language: {language}")
        return

    # Create project directory
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
        print_progress(f"Directory '{project_dir}' created.")
    else:
        print(f"{Fore.RED}Error: Directory '{project_dir}' already exists.")
        return

    # Create language-specific files
    structures[language](project_name, project_dir)
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


def setup_project():
    print(f"{Fore.YELLOW}Welcome to the setup process for Project Initializer CLI.")

    language = input(
        f"{Fore.YELLOW}Enter the default programming language for your projects (golang, typescript, rust, python): ").strip().lower()
    if not validate_language(language):
        return

    default_directory = input(
        f"{Fore.YELLOW}Enter the default directory where your projects will be created (leave blank for current directory): ").strip()
    if not default_directory:
        default_directory = os.getcwd()

    print_progress(f"Setting default language to: {language}")
    print_progress(f"Setting default project directory to: {default_directory}")
    print_progress("Setup complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Project Initializer CLI Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help="Sub-commands")

    # Define the 'run' command
    run_parser = subparsers.add_parser('run', help='Run the project initializer')
    run_parser.add_argument('--language', '-l', required=True,
                            help='Programming language (golang, typescript, rust, python)')
    run_parser.add_argument('--name', '-n', required=True, help='Project name')
    run_parser.add_argument('--dir', '-d', required=False, default=os.getcwd(),
                            help='Directory to create the project (default is current directory)')

    # Define the 'setup' command
    setup_parser = subparsers.add_parser('setup', help='Run setup tasks for the CLI tool')

    args = parser.parse_args()

    if args.command == 'run':
        language = args.language.strip().lower()
        project_name = args.name.strip()
        project_dir = os.path.join(args.dir, project_name)

        if not validate_language(language):
            return

        if not validate_project_name(project_name):
            return

        # Generate the project structure
        generate_project(language, project_name, project_dir)

    elif args.command == 'setup':
        setup_project()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
