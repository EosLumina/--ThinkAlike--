"""
Documentation Service

This module implements a system for automatically maintaining documentation
based on the current state of the codebase. It embodies our principle of
radical transparency by ensuring documentation stays in sync with code.
"""

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import markdown
from jinja2 import Environment, FileSystemLoader


class DocumentationService:
    """
    Service for automatically maintaining and updating documentation.
    
    This service implements our radical transparency principle by ensuring
    that documentation accurately reflects the current state of the codebase.
    """
    
    def __init__(self, 
                 docs_dir: str = "/workspaces/--ThinkAlike--/docs",
                 src_dir: str = "/workspaces/--ThinkAlike--"):
        """
        Initialize the documentation service.
        
        Args:
            docs_dir: Path to the documentation directory
            src_dir: Path to the source code directory
        """
        self.docs_dir = Path(docs_dir)
        self.src_dir = Path(src_dir)
        self.template_env = Environment(
            loader=FileSystemLoader(self.docs_dir / "templates")
        )
    
    def update_api_documentation(self) -> List[str]:
        """
        Update API endpoint documentation based on the current codebase.
        
        This method automatically extracts endpoint information from router
        files and updates the corresponding API documentation.
        
        Returns:
            List of updated documentation files
        """
        updated_files = []
        
        # Find all router files
        router_files = list(Path(self.src_dir / "backend/app/routes").glob("*.py"))
        
        for router_file in router_files:
            module_name = router_file.stem
            
            # Skip __init__.py and other non-router files
            if module_name.startswith("__") or not self._is_router_file(router_file):
                continue
            
            # Extract API endpoint information
            endpoints = self._extract_endpoints(router_file)
            
            if endpoints:
                # Generate API documentation
                doc_content = self._generate_api_doc(module_name, endpoints)
                
                # Determine output file path
                out_file = self.docs_dir / "architecture" / "api" / f"api_endpoints_{module_name}.md"
                out_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Write documentation file
                with open(out_file, "w") as f:
                    f.write(doc_content)
                
                updated_files.append(str(out_file))
        
        return updated_files
    
    def update_model_documentation(self) -> List[str]:
        """
        Update data model documentation based on the current codebase.
        
        This method automatically extracts model information from model
        files and updates the corresponding model documentation.
        
        Returns:
            List of updated documentation files
        """
        updated_files = []
        
        # Find all model files
        model_files = list(Path(self.src_dir / "backend/app/models").glob("*.py"))
        
        for model_file in model_files:
            module_name = model_file.stem
            
            # Skip __init__.py and other non-model files
            if module_name.startswith("__") or not self._is_model_file(model_file):
                continue
            
            # Extract model information
            models = self._extract_models(model_file)
            
            if models:
                # Generate model documentation
                doc_content = self._generate_model_doc(module_name, models)
                
                # Determine output file path
                out_file = self.docs_dir / "architecture" / "database" / f"models_{module_name}.md"
                out_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Write documentation file
                with open(out_file, "w") as f:
                    f.write(doc_content)
                
                updated_files.append(str(out_file))
        
        return updated_files
    
    def update_markdown_links(self, 
                              filename_mapping: Dict[str, str],
                              directory: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Update internal markdown links across all documentation files.
        
        This method implements our principle of radical transparency by
        ensuring documentation remains navigable after restructuring.
        
        Args:
            filename_mapping: Dictionary mapping old filenames to new filenames
            directory: Optional specific directory to update
            
        Returns:
            Dictionary mapping updated files to lists of changes made
        """
        directory = directory or self.docs_dir
        updated_files = {}
        
        # Find all markdown files
        markdown_files = list(Path(directory).glob("**/*.md"))
        
        for md_file in markdown_files:
            changes = []
            content = md_file.read_text()
            updated_content = content
            
            # Find all markdown links
            link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
            matches = link_pattern.findall(content)
            
            for link_text, link_target in matches:
                # Only process internal .md links
                if not link_target.endswith('.md'):
                    continue
                
                # Extract the filename from the path
                target_parts = link_target.split('/')
                target_filename = target_parts[-1]
                
                # Check if this filename needs to be updated
                if target_filename in filename_mapping:
                    # Create the new link target
                    new_filename = filename_mapping[target_filename]
                    
                    # Handle different path formats
                    if '/' in link_target:
                        # Replace just the filename part, preserving the path
                        new_link_target = '/'.join(target_parts[:-1] + [new_filename])
                    else:
                        # Direct link to a file in the same directory
                        new_link_target = new_filename
                    
                    # Replace the link in the content
                    old_link = f'[{link_text}]({link_target})'
                    new_link = f'[{link_text}]({new_link_target})'
                    updated_content = updated_content.replace(old_link, new_link)
                    
                    changes.append(f"Updated: {old_link} -> {new_link}")
            
            # If changes were made, write the updated content
            if content != updated_content:
                md_file.write_text(updated_content)
                updated_files[str(md_file)] = changes
        
        return updated_files
    
    def generate_api_summary(self) -> str:
        """
        Generate a summary of all API endpoints.
        
        This method creates a comprehensive overview of all API endpoints,
        supporting radical transparency by making the entire API surface 
        easily understandable.
        
        Returns:
            Path to the generated summary file
        """
        # Find all API documentation files
        api_docs = list(Path(self.docs_dir / "architecture" / "api").glob("api_endpoints_*.md"))
        
        # Extract endpoint information from each file
        endpoints_by_category = {}
        
        for api_doc in api_docs:
            category = api_doc.stem.replace("api_endpoints_", "")
            endpoints = self._extract_endpoints_from_doc(api_doc)
            
            if endpoints:
                endpoints_by_category[category] = endpoints
        
        # Generate summary documentation
        template = self.template_env.get_template("api_summary_template.md")
        content = template.render(
            endpoints_by_category=endpoints_by_category,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Write summary file
        out_file = self.docs_dir / "architecture" / "api" / "api_summary.md"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(out_file, "w") as f:
            f.write(content)
        
        return str(out_file)
    
    def _is_router_file(self, file_path: Path) -> bool:
        """
        Check if a file is a FastAPI router file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file is a router file, False otherwise
        """
        content = file_path.read_text()
        return "APIRouter" in content and "router" in content
    
    def _is_model_file(self, file_path: Path) -> bool:
        """
        Check if a file contains SQLAlchemy models.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file contains models, False otherwise
        """
        content = file_path.read_text()
        return "Base" in content and "Column" in content
    
    def _extract_endpoints(self, router_file: Path) -> List[Dict]:
        """
        Extract API endpoint information from a router file.
        
        Args:
            router_file: Path to the router file
            
        Returns:
            List of dictionaries containing endpoint information
        """
        endpoints = []
        content = router_file.read_text()
        
        # Find route definitions
        route_pattern = re.compile(r'@router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"].*\)')
        matches = route_pattern.findall(content)
        
        for method, path in matches:
            # Find the function that implements this endpoint
            func_pattern = re.compile(r'@router\.{}[\s\S]*?def\s+(\w+)'.format(method))
            func_match = func_pattern.search(content)
            
            if func_match:
                func_name = func_match.group(1)
                
                # Extract docstring
                docstring = self._extract_docstring(content, func_name)
                
                # Extract response model
                response_model = self._extract_response_model(content, method, path)
                
                endpoints.append({
                    "method": method.upper(),
                    "path": path,
                    "function": func_name,
                    "description": docstring,
                    "response_model": response_model
                })
        
        return endpoints
    
    def _extract_docstring(self, content: str, func_name: str) -> str:
        """
        Extract the docstring for a function.
        
        Args:
            content: File content
            func_name: Name of the function
            
        Returns:
            Docstring text or empty string if not found
        """
        pattern = re.compile(r'def\s+{}.*?\n\s*"""([\s\S]*?)"""'.format(func_name))
        match = pattern.search(content)
        
        if match:
            docstring = match.group(1).strip()
            return docstring
        
        return ""
    
    def _extract_response_model(self, content: str, method: str, path: str) -> str:
        """
        Extract the response model for an endpoint.
        
        Args:
            content: File content
            method: HTTP method
            path: Endpoint path
            
        Returns:
            Response model name or empty string if not found
        """
        pattern = re.compile(r'@router\.{}[\s\S]*?response_model=(\w+)'.format(method))
        match = pattern.search(content)
        
        if match:
            return match.group(1)
        
        return ""
    
    def _generate_api_doc(self, module_name: str, endpoints: List[Dict]) -> str:
        """
        Generate API documentation content.
        
        Args:
            module_name: Name of the API module
            endpoints: List of endpoint information
            
        Returns:
            Markdown documentation content
        """
        template = self.template_env.get_template("api_doc_template.md")
        return template.render(
            module_name=module_name,
            endpoints=endpoints,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _extract_models(self, model_file: Path) -> List[Dict]:
        """
        Extract model information from a model file.
        
        Args:
            model_file: Path to the model file
            
        Returns:
            List of dictionaries containing model information
        """
        models = []
        content = model_file.read_text()
        
        # Find class definitions
        class_pattern = re.compile(r'class\s+(\w+)\(Base\):')
        matches = class_pattern.findall(content)
        
        for model_name in matches:
            # Extract tablename
            tablename_pattern = re.compile(r'class\s+{}.*?__tablename__\s*=\s*[\'"]([^\'"]+)[\'"]'.format(model_name))
            tablename_match = tablename_pattern.search(content)
            tablename = tablename_match.group(1) if tablename_match else ""
            
            # Extract docstring
            docstring_pattern = re.compile(r'class\s+{}.*?\n\s*"""([\s\S]*?)"""'.format(model_name))
            docstring_match = docstring_pattern.search(content)
            docstring = docstring_match.group(1).strip() if docstring_match else ""
            
            # Extract columns
            column_pattern = re.compile(r'(\w+)\s*=\s*Column\((.*?)\)')
            column_matches = column_pattern.findall(content)
            
            columns = []
            for column_name, column_def in column_matches:
                columns.append({
                    "name": column_name,
                    "definition": column_def.strip()
                })
            
            models.append({
                "name": model_name,
                "tablename": tablename,
                "description": docstring,
                "columns": columns
            })
        
        return models
    
    def _generate_model_doc(self, module_name: str, models: List[Dict]) -> str:
        """
        Generate model documentation content.
        
        Args:
            module_name: Name of the model module
            models: List of model information
            
        Returns:
            Markdown documentation content
        """
        template = self.template_env.get_template("model_doc_template.md")
        return template.render(
            module_name=module_name,
            models=models,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _extract_endpoints_from_doc(self, doc_file: Path) -> List[Dict]:
        """
        Extract endpoint information from a documentation file.
        
        Args:
            doc_file: Path to the documentation file
            
        Returns:
            List of dictionaries containing endpoint information
        """
        endpoints = []
        content = doc_file.read_text()
        
        # Find endpoint sections
        endpoint_pattern = re.compile(r'## (\w+) `(GET|POST|PUT|DELETE|PATCH) ([^`]+)`')
        matches = endpoint_pattern.findall(content)
        
        for func_name, method, path in matches:
            # Extract description
            desc_pattern = re.compile(r'## {}.*?\n\n(.*?)\n\n'.format(func_name))
            desc_match = desc_pattern.search(content)
            description = desc_match.group(1) if desc_match else ""
            
            endpoints.append({
                "method": method,
                "path": path,
                "function": func_name,
                "description": description
            })
        
        return endpoints