#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Common fixes for markdown files
const fixes = {
  // Convert dash lists to asterisk lists
  dashToAsterisk: (content) => {
    return content.replace(/^(\s*)-\s+/gm, '$1* ');
  },
  
  // Fix list marker spacing
  fixListSpacing: (content) => {
    return content.replace(/^(\s*[*+-])\s{2,}/gm, '$1 ');
  },
  
  // Ensure blank lines around lists
  blankLinesAroundLists: (content) => {
    // Add blank line before lists that don't have one
    content = content.replace(/([^\n])\n^(\s*[*+-])/gm, '$1\n\n$2');
    // Add blank line after lists
    content = content.replace(/^(\s*[*+-][^\n]+)\n([^*+-\s\n])/gm, '$1\n\n$2');
    return content;
  },
  
  // Fix headings (ensure proper format and spacing)
  fixHeadings: (content) => {
    // Ensure space after # in headers
    content = content.replace(/^(#+)([^ #])/gm, '$1 $2');
    // Add blank line before headings
    content = content.replace(/([^\n])\n(#+\s+)/g, '$1\n\n$2');
    // Add blank line after headings
    content = content.replace(/(#+\s+[^\n]+)(\n[^#\n])/g, '$1\n\n$2');
    return content;
  },
  
  // Fix blank lines around code blocks
  fixCodeBlockBlankLines: (content) => {
    // Add blank line before code blocks
    content = content.replace(/([^\n])\n(```)/g, '$1\n\n$2');
    // Add blank line after code blocks
    content = content.replace(/(```[^\n]*\n[\s\S]*?\n```)(\n[^`\n])/g, '$1\n\n$2');
    return content;
  },
  
  // Ensure single trailing newline
  ensureTrailingNewline: (content) => {
    return content.replace(/\n*$/, '\n');
  }
};

// Function to fix markdown linting issues
function fixMarkdownLinting(content) {
  // 1. Fix multiple blank lines (MD012)
  content = content.replace(/\n{3,}/g, '\n\n');

  // 2. Fix line length (MD013) - This is a complex fix and would require manual editing
  // We'll just add a comment to the file about this

  // 3. Fix trailing spaces (MD009)
  content = content.replace(/ +$/gm, '');

  // 4. Fix spaces inside emphasis markers (MD037)
  content = content.replace(/\*\* ([^*]+) \*\*/g, '**$1**');
  content = content.replace(/\* ([^*]+) \*/g, '*$1*');

  // 5. Fix spaces inside code span elements (MD038)
  content = content.replace(/` ([^`]+) `/g, '`$1`');

  // 6. Fix ordered list item prefix issues (MD029)
  // This is complex and might need manual fixing

  // Add a comment about line length issues at the top of the file
  if (content.includes('MD013/line-length')) {
    content = `<!-- 
NOTE: This file has markdown linting issues related to line length (MD013).
Consider breaking long lines when editing this file.
-->\n\n${content}`;
  }

  return content;
}

// Process a file
function processFile(filePath) {
  console.log(`Processing ${filePath}`);
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Apply fixes
  content = fixes.dashToAsterisk(content);
  content = fixes.fixListSpacing(content);
  content = fixes.blankLinesAroundLists(content);
  content = fixes.fixHeadings(content);
  content = fixes.fixCodeBlockBlankLines(content);
  content = fixes.ensureTrailingNewline(content);
  content = fixMarkdownLinting(content);
  
  // Write fixed content back
  fs.writeFileSync(filePath, content);
}

// Find all markdown files
function findMarkdownFiles(dir) {
  const files = [];
  fs.readdirSync(dir, { withFileTypes: true }).forEach(dirent => {
    const res = path.resolve(dir, dirent.name);
    if (dirent.isDirectory()) {
      if (dirent.name !== 'node_modules' && dirent.name !== '.git') {
        files.push(...findMarkdownFiles(res));
      }
    } else if (dirent.name.endsWith('.md')) {
      files.push(res);
    }
  });
  return files;
}

// Main
const markdownFiles = findMarkdownFiles('/workspaces/--ThinkAlike--');
console.log(`Found ${markdownFiles.length} Markdown files to process`);
markdownFiles.forEach(processFile);
console.log(`Processed ${markdownFiles.length} files`);

// Fix the copilot-instructions.md file
const filePath = '/workspaces/--ThinkAlike--/.github/copilot-instructions.md';
processFile(filePath);
console.log('Fixed markdown linting issues in copilot-instructions.md');
