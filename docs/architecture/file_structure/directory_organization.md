# ThinkAlike Directory Organization

This document outlines the organization of the ThinkAlike project files, embodying our principles of digital sovereignty through clear boundaries and explicit structure.

## Root Directory

The root directory contains essential configuration files and entry points:

- **.env.example / .env**: Environment configuration (not committed to git)
- **.gitconfig / .gitignore**: Git configuration
- **mkdocs.yml**: Documentation generator configuration
- **package.json**: JavaScript dependencies
- **pyproject.toml**: Python project configuration
- **setup.py**: Python package setup
- **README.md**: Project overview

## Key Directories

### `/backend`

Contains the Python backend application:

- **app/**: Application code
  - **services/**: Business logic services
    - **documentation_sovereignty.py**: Implementation of documentation integrity verification

### `/docs`

The documentation knowledge commons, organized by domain:

- **core/**: Fundamental principles and concepts
- **architecture/**: System design and structure
- **vision/**: Project goals and manifestos

### `/scripts`

Utility scripts for project maintenance and operations.

### `/data`

Project data storage with clear boundaries from code.

### `/backups`

Historical snapshots of project state.

## Sovereign Boundary Principles

This organization embodies our commitment to:

1. **Clear Domain Separation**: Each directory has a distinct, well-defined purpose
2. **Explicit Boundaries**: The relationships between domains are clear and documented
3. **Minimal Root Clutter**: Essential files only in the root, with specialized files in appropriate directories
4. **Sovereign Documentation**: Documentation remains in its own domain, separate from implementation
5. **Traceable History**: Backup preservation ensures knowledge history remains sovereign

This structure is not merely organizational but philosophical - a rejection of the digital entropy that conventional systems allow, and an assertion that clear boundaries enhance rather than restrict human autonomy.
