# Project Initializer CLI Tool (P.I.C.T)

## Overview

**Project Initializer** is a command-line tool designed to help developers quickly scaffold production-ready project structures for different programming languages, including **Golang**, **TypeScript**, **Rust**, and **Python**.

The tool automatically generates folder structures, creates essential configuration files like **Dockerfiles**, **Makefiles**, **.gitignore**, and **.env** files, and sets up the project with modern best practices.

## Features

- Supports **Golang**, **TypeScript**, **Rust**, and **Python**.
- Generates a production-ready folder structure.
- Creates **Dockerfile** with Alpine-based images for lightweight Docker builds.
- Adds **Makefile** with build, run, and Docker commands.
- Sets up **.env** files for environment variables.
- Adds language-specific **.gitignore** files.
- Simple and easy-to-use command-line interface (CLI).

## Installation

To install the Project Initializer CLI tool, use `pip`:

```bash
pip install pict
