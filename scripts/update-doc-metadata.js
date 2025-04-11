#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Get the current date in YYYY-MM-DD format
const currentDate = new Date().toISOString().split('T')[0];

// Function to get Git last modified date for a file
function getGitLastModified(filePath) {
  try {
    // Get relative path for Git commands
    const relativePath = path.relative('/workspaces/--ThinkAlike--', filePath);
    
    // Get the last commit date for this file
    const gitDate = execSync(
      `git log -1 --format="%ad" --date=short -- "${relativePath}"`, 
      { encoding: 'utf8', cwd: '/workspaces/--ThinkAlike--' }
    ).trim();
    
    return gitDate || currentDate; // Return git date or current date as fallback
  } catch (error) {
    console.log(`Could not get git history for ${filePath}: ${error.message}`);
    return currentDate; // Fallback to current date
  }
}

// Function to update document metadata in a file
function updateDocMetadata(filePath) {
  try {
    // Read the file content
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Get the last modified date from Git
    const lastModifiedDate = getGitLastModified(filePath);
    
    // Replace future dates in metadata with git last modified date
    let updatedContent = content.replace(
      /- Last Updated: 202[0-9]-[0-9]{2}-[0-9]{2}/g,
      `- Last Modified: ${lastModifiedDate}`
    );
    
    // Also replace "Last Updated" with "Last Modified" for consistency
    updatedContent = updatedContent.replace(
      /- Last Updated:/g,
      '- Last Modified:'
    );
    
    // Write back to the file if changed
    if (content !== updatedContent) {
      fs.writeFileSync(filePath, updatedContent);
      console.log(`Updated metadata in: ${filePath}`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error(`Error processing file ${filePath}:`, error);
    return false;
  }
}

// Function to recursively find markdown files
function findMarkdownFiles(dir) {
  const files = [];
  
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        if (entry.name !== 'node_modules' && entry.name !== '.git') {
          files.push(...findMarkdownFiles(fullPath));
        }
      } else if (entry.name.endsWith('.md')) {
        files.push(fullPath);
      }
    }
  } catch (error) {
    console.error(`Error reading directory ${dir}:`, error);
  }
  
  return files;
}

// Main execution
const rootDir = '/workspaces/--ThinkAlike--';
console.log('Finding Markdown files...');
const markdownFiles = findMarkdownFiles(rootDir);
console.log(`Found ${markdownFiles.length} Markdown files`);

let updatedCount = 0;
for (const file of markdownFiles) {
  if (updateDocMetadata(file)) {
    updatedCount++;
  }
}

console.log(`Updated metadata in ${updatedCount} files`);
console.log('Document metadata update completed');
