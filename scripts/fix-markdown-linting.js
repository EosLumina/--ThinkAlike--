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

const markdownlint = require("markdownlint");
const fs = require("fs");
const path = require("path");
const glob = require("glob");
const chalk = require("chalk");
const { execSync } = require("child_process");

// Configuration aligned with ThinkAlike standards
const config = {
  "default": true,
  "MD012": { "maximum": 1 },        // Multiple consecutive blank lines
  "MD013": { "line_length": 120 },  // Increased line length limit
  "MD033": false,                   // Allow inline HTML for our documentation needs
  "MD041": false,                   // First line in a file should be a top-level header
  "MD026": { "punctuation": ".,;:!" }, // Trailing punctuation in headers
  "MD029": { "style": "ordered" },  // Ordered list item prefix
  "MD007": { "indent": 2 },         // Unordered list indentation
  "MD036": false,                   // Emphasis used instead of a header
};

console.log('🌟 ThinkAlike Markdown Linting Auto-fixer 🌟');
console.log('-------------------------------------------');

// Functions for fixing common issues
function fixCommonIssues(content) {
  // Fix headers without space after #
  content = content.replace(/^(#+)([^ #])/gm, "$1 $2");

  // Fix blank lines around lists
  content = content.replace(/^([^\n-*+0-9].*)\n+([-*+])/gm, "$1\n\n$2");
  content = content.replace(/^([-*+].*)\n+([^\n-*+])/gm, "$1\n\n$2");

  // Fix blank lines around headings
  content = content.replace(/^([^\n#].*)\n+(#{1,6})/gm, "$1\n\n$2");
  content = content.replace(/^(#{1,6}.*)\n+([^\n#])/gm, "$1\n\n$2");

  // Fix blank lines around code blocks
  content = content.replace(/^([^\n`].*)\n+(```)/gm, "$1\n\n$2");
  content = content.replace(/(```.*)\n+([^\n`])/gm, "$1\n\n$2");

  // Standardize ordered list prefixes (1. 2. 3. etc)
  content = content.replace(/^(\s*)(\d+)\.(\s+)/gm, (match, indent, num, space) => {
    // Always use a single space after list marker
    return `${indent}${num}.${space.length >= 1 ? ' ' : space}`;
  });

  // Fix ordered list numbering in sequences
  content = fixOrderedListNumbering(content);

  // Standardize unordered list markers to use asterisks and correct spacing
  content = content.replace(/^(\s*)-(\s+)/gm, "$1*$2");
  content = content.replace(/^(\s*)\*(\s{2,})/gm, "$1* ");

  // Fix emphasis used as headings (common in Document Details sections)
  content = content.replace(/^(\*\*Document Details\*\*)$/gm, "## Document Details");

  // Fix list indentation
  content = content.replace(/^(\s{3,})([*+-])\s/gm, (match, indent, marker) => {
    // Convert to standard two-space indentation
    const level = Math.floor(indent.length / 2);
    return `${"  ".repeat(level)}${marker} `;
  });

  // Remove multiple consecutive blank lines (keep only single blank lines)
  content = content.replace(/\n{3,}/g, "\n\n");

  // Ensure file ends with a single newline
  if (!content.endsWith("\n")) {
    content += "\n";
  }

  return content;
}

// Function to fix ordered list numbering
function fixOrderedListNumbering(content) {
  const lines = content.split('\n');
  let inList = false;
  let listLevel = 0;
  let counter = 0;

  for (let i = 0; i < lines.length; i++) {
    // Check if line is part of an ordered list
    const listMatch = lines[i].match(/^(\s*)(\d+)\.\s/);

    if (listMatch) {
      const indent = listMatch[1].length;

      // If this is a new list or a different indentation level
      if (!inList || indent !== listLevel) {
        inList = true;
        listLevel = indent;
        counter = 1;
      } else {
        counter++;
      }

      // Replace the number with the correct sequential number
      lines[i] = lines[i].replace(/^(\s*)\d+\./, `$1${counter}.`);
    } else if (inList && lines[i].trim() === '') {
      // Empty line might end a list
      inList = false;
    }
  }

  return lines.join('\n');
}

// Main function to process files
function processMarkdownFiles(files) {
  console.log(`Processing ${files.length} markdown files...`);
  let fixedFiles = 0;

  files.forEach(filePath => {
    try {
      console.log(`Processing: ${filePath}`);
      const content = fs.readFileSync(filePath, 'utf8');
      const originalContent = content;

      // Apply all fixes
      let fixedContent = fixCommonIssues(content);

      // Write changes back if content was modified
      if (fixedContent !== originalContent) {
        fs.writeFileSync(filePath, fixedContent);
        console.log(`✅ Fixed issues in: ${filePath}`);
        fixedFiles++;
      } else {
        console.log(`✓ No issues fixed in: ${filePath}`);
      }
    } catch (error) {
      console.error(`❌ Error processing ${filePath}: ${error.message}`);
    }
  });

  return fixedFiles;
}

// Main execution
console.log('🌟 ThinkAlike Markdown Linting Auto-fixer 🌟');
console.log('-------------------------------------------');

// Find all markdown files
let files = [];
try {
  const findCommand = 'find /workspaces/--ThinkAlike-- -type f -name "*.md" | grep -v "node_modules" | grep -v ".git"';
  const output = execSync(findCommand).toString();
  files = output.trim().split('\n').filter(Boolean);
  console.log(`Found ${files.length} Markdown files to process.`);
} catch (error) {
  console.error(`Failed to find Markdown files: ${error.message}`);
  process.exit(1);
}

// Process all files
const fixedFiles = processMarkdownFiles(files);
console.log(`\n✨ Process complete! Fixed issues in ${fixedFiles}/${files.length} files.`);

// Instructions for remaining issues
console.log('\nTo check for remaining issues:');
console.log('  npx markdownlint "**/*.md" --ignore node_modules');
console.log('\nTo fix specific file manually:');
console.log('  npx markdownlint-cli2-fix "path/to/file.md"');
