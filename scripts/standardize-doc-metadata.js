#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Function to get git last modified date for a file
function getGitLastModified(filePath) {
  try {
    const relativePath = path.relative('/workspaces/--ThinkAlike--', filePath);
    const gitDate = execSync(`git log -1 --format="%ad" --date=short -- ${relativePath}`, { 
      encoding: 'utf8',
      cwd: '/workspaces/--ThinkAlike--'
    }).trim();
    
    return gitDate || new Date().toISOString().split('T')[0]; // Fallback to current date
  } catch (error) {
    console.error(`Error getting git date for ${filePath}:`, error);
    return new Date().toISOString().split('T')[0]; // Fallback to current date
  }
}

// Function to standardize document metadata
function standardizeMetadata(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  
  // Check if file already has metadata section
  const metadataRegex = /---\s*\*\*Document Details\*\*.*?---\s*$/s;
  const lastModifiedDate = getGitLastModified(filePath);
  
  // Get document title from first heading if available
  let title = path.basename(filePath, '.md');
  const titleMatch = content.match(/^#\s+(.+)$/m);
  if (titleMatch) {
    title = titleMatch[1];
  }
  
  // Determine document type based on path
  let docType = "Documentation";
  if (filePath.includes('/guides/')) {
    docType = "Guide";
  } else if (filePath.includes('/core/')) {
    docType = "Core Documentation";
  } else if (filePath.includes('/architecture/')) {
    docType = "Architecture Documentation";
  } else if (filePath.includes('/components/')) {
    docType = "Component Specification";
  }
  
  // Create new metadata
  const newMetadata = `
---
**Document Details**
- Title: ${title}
- Type: ${docType}
- Version: 1.0.0
- Last Modified: ${lastModifiedDate} (via git history)
---
`;

  let updatedContent;
  if (metadataRegex.test(content)) {
    // Replace existing metadata
    updatedContent = content.replace(metadataRegex, newMetadata.trim());
  } else {
    // Add metadata at the end
    updatedContent = content.trim() + "\n\n" + newMetadata;
  }
  
  fs.writeFileSync(filePath, updatedContent);
  return true;
}

// Main function
function main() {
  const rootDir = '/workspaces/--ThinkAlike--';
  const docsDir = path.join(rootDir, 'docs');
  
  // Find all markdown files in the docs directory
  function findMarkdownFiles(dir) {
    const files = [];
    fs.readdirSync(dir, { withFileTypes: true }).forEach(dirent => {
      const filePath = path.join(dir, dirent.name);
      if (dirent.isDirectory()) {
        files.push(...findMarkdownFiles(filePath));
      } else if (dirent.name.endsWith('.md')) {
        files.push(filePath);
      }
    });
    return files;
  }
  
  const markdownFiles = findMarkdownFiles(docsDir);
  console.log(`Found ${markdownFiles.length} markdown files`);
  
  let updatedCount = 0;
  markdownFiles.forEach(file => {
    if (standardizeMetadata(file)) {
      updatedCount++;
    }
  });
  
  console.log(`Standardized metadata in ${updatedCount} files`);
}

main();
