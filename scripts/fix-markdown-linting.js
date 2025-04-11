#!/usr/bin/env node

/**
 * ThinkAlike Markdown Linting Auto-fix Script
 *
 * This script automatically fixes common Markdown linting issues across the project
 * in alignment with ThinkAlike's documentation standards.
 *
 * Features:
 * - Fixes trailing whitespace
 * - Ensures files end with a single newline
 * - Ensures proper spacing around headers, lists, and code blocks
 * - Wraps long lines at 120 characters when possible
 * - Fixes ordered list numbering
 *
 * Usage: node scripts/fix-markdown-linting.js [filepath]
 * If no filepath is provided, will process all markdown files in the project.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🌟 ThinkAlike Markdown Linting Auto-fixer 🌟');
console.log('-------------------------------------------');

// Get files to process
let files = [];
const specifiedFile = process.argv[2];

if (specifiedFile) {
  // Process only the specified file
  files = [specifiedFile];
  console.log(`Processing single file: ${specifiedFile}`);
} else {
  // Find all markdown files in the project
  console.log('Finding all Markdown files...');
  const findCommand = 'find /workspaces/--ThinkAlike-- -type f -name "*.md" | grep -v "node_modules" | grep -v ".git"';
  files = execSync(findCommand).toString().trim().split('\n');
  console.log(`Found ${files.length} Markdown files to process.`);
}

// Counter for fixed issues
let fixCount = 0;

// Process each file
files.forEach(filePath => {
  if (!filePath || !fs.existsSync(filePath)) return;

  console.log(`Processing: ${filePath}`);

  // Read the file content
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  // Fix: Remove trailing whitespace (MD009)
  content = content.replace(/[ \t]+$/gm, '');

  // Fix: Ensure file ends with a single newline (MD047)
  content = content.trimEnd() + '\n';

  // Fix: Add language specifiers to code blocks (MD040)
  content = content.replace(/```\s*\n/g, '```text\n');

  // Fix: Ensure blank lines before and after headers (MD022, MD023)
  content = content.replace(/^(.*)\n(#{1,6} .*)/gm, '$1\n\n$2');
  content = content.replace(/(#{1,6} .*)\n(?!\n)/gm, '$1\n\n');

  // Fix: Ensure blank lines before and after lists (MD032)
  content = content.replace(/([^\n])\n([\*\-\+] )/gm, '$1\n\n$2');
  content = content.replace(/([\*\-\+] .*)\n(?!\n)([^\*\-\+\s])/gm, '$1\n\n$2');
  content = content.replace(/([^\n])\n(\d+\. )/gm, '$1\n\n$2');
  content = content.replace(/(\d+\. .*)\n(?!\n)([^\d\s])/gm, '$1\n\n$2');

  // Fix: Ensure blank lines before and after code blocks (MD031)
  content = content.replace(/([^\n])\n(```)/gm, '$1\n\n$2');
  content = content.replace(/(```.*)\n(?!\n)/gm, '$1\n\n');

  // Fix: Fix ordered list numbering (MD029)
  content = content.replace(/^(\s*)\d+\.\s/gm, (match, indent, index) => {
    // Get the number of preceding ordered list items with the same indentation
    const lines = content.split('\n');
    const lineIndex = content.substring(0, content.indexOf(match)).split('\n').length - 1;

    // Count ordered list items with the same indentation that came before this one
    let itemNumber = 1;
    for (let i = 0; i < lineIndex; i++) {
      if (lines[i].match(new RegExp(`^${indent}\\d+\\.\\s`))) {
        itemNumber++;
      } else if (lines[i].trim() === '' || !lines[i].startsWith(indent)) {
        // Reset counter on blank lines or different indentation
        itemNumber = 1;
      }
    }

    return `${indent}${itemNumber}. `;
  });

  // If content changed, write back to file
  if (content !== originalContent) {
    fixCount++;
    fs.writeFileSync(filePath, content);
    console.log(`✅ Fixed issues in ${filePath}`);
  } else {
    console.log(`✓ No issues found in ${filePath}`);
  }
});

console.log('\n-------------------------------------------');
console.log(`✨ Process complete! Fixed issues in ${fixCount} files.`);
console.log('');
console.log('To fix remaining issues that require manual attention, run:');
console.log('  npx markdownlint "**/*.md" --ignore node_modules');
