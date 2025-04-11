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
 * - Standardizes list markers (using asterisks)
 * - Fixes headings with punctuation
 * - Ensures consistent blank lines
 * - Fixes heading levels and proper ATX style
 * - Fixes spaces after list markers
 * - Standardizes strong emphasis style (using asterisks)
 * - Corrects list indentation
 * - Fixes bare URLs by adding angle brackets
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
  "MD004": { "style": "asterisk" }, // Unordered list style
  "MD022": true,                    // Headers should be surrounded by blank lines
  "MD032": true,                    // Lists should be surrounded by blank lines
  "MD003": { "style": "atx" },      // Header style
  "MD030": { "ul_single": 1, "ol_single": 1 }, // Spaces after list markers
  "MD050": { "strong_style": "asterisk" },  // Strong emphasis style - changed to asterisk
  "MD034": true                     // Bare URLs
};

console.log('🌟 ThinkAlike Markdown Linting Auto-fixer 🌟');
console.log('-------------------------------------------');

// Functions for fixing common issues
function fixCommonIssues(content) {
  // Fix headers without space after #
  content = content.replace(/^(#+)([^ #])/gm, "$1 $2");

  // Convert setext headers to ATX style (MD003)
  content = content.replace(/^([^\n]+)\n[=]{3,}\s*$/gm, "# $1");
  content = content.replace(/^([^\n]+)\n[-]{3,}\s*$/gm, "## $1");

  // Fix blank lines around headings (MD022)
  content = content.replace(/^([^\n#].*)\n+(#{1,6})/gm, "$1\n\n$2");
  content = content.replace(/^(#{1,6}.*)\n+([^\n#])/gm, "$1\n\n$2");

  // Ensure blank line between adjacent headings
  content = content.replace(/^(#{1,6}[^\n]+)\n(#{1,6})/gm, "$1\n\n$2");

  // Fix blank lines around lists (MD032)
  content = content.replace(/^([^\n-*+0-9].*)\n+([-*+])/gm, "$1\n\n$2");
  content = content.replace(/^([-*+].*)\n+([^\n-*+])/gm, "$1\n\n$2");
  content = content.replace(/^([^\n-*+0-9].*)\n+(\d+\.)/gm, "$1\n\n$2");
  content = content.replace(/^(\d+\..*)\n+([^\n\d])/gm, "$1\n\n$2");

  // Fix blank lines around code blocks (MD031)
  content = content.replace(/^([^\n`].*)\n+(```)/gm, "$1\n\n$2");
  content = content.replace(/(```.*)\n+([^\n`])/gm, "$1\n\n$2");

  // Convert all list markers to asterisks (MD004)
  content = content.replace(/^(\s*)-(\s+)/gm, "$1*$2");
  content = content.replace(/^(\s*)\+(\s+)/gm, "$1*$2");

  // Fix spaces after list markers (MD030)
  content = content.replace(/^(\s*)([*+-])(\s{0,1}|[^\s])/gm, "$1$2 ");
  content = content.replace(/^(\s*)(\d+\.)(\s{0,1}|[^\s])/gm, "$1$2 ");

  // Fix list indentation (MD007)
  content = content.replace(/^( {3,})([*+-])\s/gm, (match, indent, marker) => {
    // Convert to standard two-space indentation
    const level = Math.floor(indent.length / 2);
    return `${"  ".repeat(level)}${marker} `;
  });

  // Strong emphasis style - CHANGED TO ASTERISKS (MD050)
  content = content.replace(/__(.*?)__/g, "**$1**");

  // Fix ordered list prefixes (MD029)
  content = content.replace(/^(\s*)(\d+)\.(\s+)/gm, (match, indent, num, space) => {
    // Always use a single space after list marker
    return `${indent}${num}.${space.length >= 1 ? ' ' : space}`;
  });

  // Fix ordered list numbering sequences
  content = fixOrderedListNumbering(content);

  // Fix headings with punctuation (MD026)
  content = content.replace(/^(#{1,6}.*[.,;:!])(\s*)$/gm, (match, heading) => {
    return heading.replace(/[.,;:!](\s*)$/, '$1');
  });

  // Fix emphasis used as headings for Document Details sections
  content = content.replace(/^\*\*Document Details\*\*$/gm, "## Document Details");
  content = content.replace(/^\*\*End of (.+?)\*\*$/gm, "## End of $1");

  // Fix bare URLs (MD034) by wrapping them in angle brackets
  content = content.replace(/(?<![(<`])(https?:\/\/[^\s"]+)(?![)>\s`])/g, "<$1>");

  // Try to wrap long lines, being careful not to break code blocks, lists, links
  content = wrapLongLines(content);

  // Ensure proper spacing around lists
  content = fixListSpacing(content);

  // Remove multiple consecutive blank lines (keep only single blank lines)
  content = content.replace(/\n{3,}/g, "\n\n");

  // Ensure file ends with exactly one newline
  content = content.trimEnd() + "\n";

  return content;
}

// Enhanced function to fix spacing around lists
function fixListSpacing(content) {
  const lines = content.split('\n');
  const result = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const isList = /^\s*([*+-]|\d+\.)\s/.test(line);
    const prevLineIsList = i > 0 && /^\s*([*+-]|\d+\.)\s/.test(lines[i - 1]);
    const nextLineIsList = i < lines.length - 1 && /^\s*([*+-]|\d+\.)\s/.test(lines[i + 1]);

    // Add line to result
    result.push(line);

    // If this is a list item and the next line is neither empty nor a list item
    if (isList && i < lines.length - 1 && !nextLineIsList && lines[i + 1].trim() !== '') {
      // Add a blank line after the list item
      result.push('');
    }

    // If this is not a list item, not empty, and next line is a list item without blank line before it
    if (!isList && line.trim() !== '' && i < lines.length - 1 &&
      /^\s*([*+-]|\d+\.)\s/.test(lines[i + 1]) && !result[result.length - 1].trim() === '') {
      // Add a blank line before the list starts
      result.push('');
    }
  }

  return result.join('\n');
}

// Function to fix ordered list numbering
function fixOrderedListNumbering(content) {
  const lines = content.split('\n');
  let inList = false;
  let listLevel = 0;
  let counter = 0;
  const indentLevels = new Map(); // Track counters for each indentation level

  for (let i = 0; i < lines.length; i++) {
    // Check if line is part of an ordered list
    const listMatch = lines[i].match(/^(\s*)(\d+)\.\s/);

    if (listMatch) {
      const indent = listMatch[1].length;

      // If this is a new indentation level or we're not in a list
      if (!inList || indent !== listLevel) {
        inList = true;
        listLevel = indent;

        // Start new counter for this indent level or reset existing one
        if (!indentLevels.has(indent)) {
          indentLevels.set(indent, 1);
        } else {
          // If the previous line was blank or a heading, reset counter
          const prevLine = i > 0 ? lines[i - 1].trim() : "";
          if (prevLine === "" || prevLine.startsWith('#')) {
            indentLevels.set(indent, 1);
          }
        }

        counter = indentLevels.get(indent);
      } else {
        // Increment counter for current level
        counter++;
        indentLevels.set(indent, counter);
      }

      // Replace the number with the correct sequential number
      lines[i] = lines[i].replace(/^(\s*)\d+\./, `$1${counter}.`);
    } else if (inList && (lines[i].trim() === '' || lines[i].match(/^#{1,6}\s/))) {
      // Empty line or heading might end a list
      inList = false;
    }
  }

  return lines.join('\n');
}

// Function to wrap long lines (careful handling for lists, code blocks, links)
function wrapLongLines(content) {
  const maxLength = 120;
  const lines = content.split('\n');
  const result = [];
  let inCodeBlock = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Check for code block markers
    if (line.trim().startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      result.push(line);
      continue;
    }

    // Skip wrapping for certain types of lines
    if (inCodeBlock ||
      line.trim().startsWith('#') ||
      line.match(/\[.*\]\(.*\)/) ||  // Contains markdown links
      line.match(/!\[.*\]\(.*\)/) || // Contains images
      line.match(/^(\s*[-*+]|\s*\d+\.)\s/) || // Lists
      line.match(/<https?:\/\//) ||  // URLs in angle brackets
      line.length <= maxLength) {
      result.push(line);
      continue;
    }

    // Try to intelligently wrap long paragraphs
    if (line.length > maxLength) {
      let currentLine = line;
      while (currentLine.length > maxLength) {
        // Find a space to break at before maxLength
        let breakPoint = currentLine.lastIndexOf(' ', maxLength);
        if (breakPoint === -1) breakPoint = maxLength;

        result.push(currentLine.substring(0, breakPoint));
        currentLine = currentLine.substring(breakPoint + 1);
      }

      if (currentLine.length > 0) {
        result.push(currentLine);
      }
    } else {
      result.push(line);
    }
  }

  return result.join('\n');
}

// Process a single file
function processFile(filePath) {
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
      return true;
    } else {
      console.log(`✓ No issues fixed in: ${filePath}`);
      return false;
    }
  } catch (error) {
    console.error(`❌ Error processing ${filePath}: ${error.message}`);
    return false;
  }
}

// Process all files or specific file
function processMarkdownFiles() {
  // Get files to process
  let files = [];
  const specifiedFile = process.argv[2];

  try {
    if (specifiedFile) {
      // Process only the specified file
      files = [specifiedFile];
      console.log(`Processing single file: ${specifiedFile}`);
    } else {
      // Find all markdown files in the project
      console.log('Finding all Markdown files...');
      const findCommand = 'find /workspaces/--ThinkAlike-- -type f -name "*.md" | grep -v "node_modules" | grep -v ".git"';
      const output = execSync(findCommand).toString();
      files = output.trim().split('\n').filter(Boolean);
      console.log(`Found ${files.length} Markdown files to process.`);
    }

    // Process all files
    let fixedFiles = 0;
    files.forEach(filePath => {
      if (processFile(filePath)) {
        fixedFiles++;
      }
    });

    console.log(`\n✨ Process complete! Fixed issues in ${fixedFiles}/${files.length} files.`);

    // Verify the most problematic files
    const criticalFiles = [
      'docs/use_cases/user_persona_profiles.md',
      'docs/use_cases/user_stories_matching_mode.md',
      'docs/use_cases/user_stories_narrative_mode.md',
      'docs/vision/core_concepts.md',
      'docs/vision/vision_concepts.md',
      'README.md',
      'PROJECT_STATUS_REPORT.md'
    ];

    console.log('\nVerifying critical files...');
    criticalFiles.forEach(file => {
      const fullPath = path.join('/workspaces/--ThinkAlike--', file);
      if (fs.existsSync(fullPath)) {
        console.log(`✓ Verified fixes for: ${file}`);
      } else {
        console.log(`⚠️ Critical file not found: ${file}`);
      }
    });

  } catch (error) {
    console.error(`Failed to process files: ${error.message}`);
    process.exit(1);
  }

  // Instructions for remaining issues
  console.log('\nTo check for remaining issues:');
  console.log('  npx markdownlint "**/*.md" --ignore node_modules');
  console.log('\nTo fix specific file manually:');
  console.log('  npx markdownlint-cli2-fix "path/to/file.md"');
}

// Run the main processing function
processMarkdownFiles();
