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
    // Ensure exactly one space after list marker
    content = content.replace(/^(\s*[*+-])\s{2,}/gm, '$1 ');
    // Ensure there is at least one space after list marker
    content = content.replace(/^(\s*[*+-])([^\s])/gm, '$1 $2');
    return content;
  },

  // Ensure blank lines around lists
  blankLinesAroundLists: (content) => {
    // Add blank line before lists that don't have one and aren't the first line
    content = content.replace(/(?<=\n)([^\n\s])\n(\s*[*+-])/g, '$1\n\n$2');
    // Add blank line after lists that aren't followed by another list item or end of file
    content = content.replace(/(\n\s*[*+-][^\n]+)\n([^\s*+-\n])/g, '$1\n\n$2');
    return content;
  },

  // Fix headings (ensure proper format and spacing)
  fixHeadings: (content) => {
    // Ensure space after # in headers
    content = content.replace(/^(#+)([^ #\n])/gm, '$1 $2');
    // Add blank line before headings (unless it's the first line)
    content = content.replace(/(?<=\n)([^\n])\n(#+\s+)/g, '$1\n\n$2');
    // Add blank line after headings (unless followed by another heading or end of file)
    content = content.replace(/(#+\s+[^\n]+)\n([^#\n\s])/g, '$1\n\n$2');
    return content;
  },

  // Fix blank lines around code blocks
  fixCodeBlockBlankLines: (content) => {
    // Add blank line before code blocks (unless it's the first line)
    content = content.replace(/(?<=\n)([^\n])\n(```)/g, '$1\n\n$2');
    // Add blank line after code blocks (unless followed by end of file)
    content = content.replace(/(```[^\n]*\n[\s\S]*?\n```)\n([^\n`])/g, '$1\n\n$2');
    return content;
  },

  // Ensure single trailing newline
  ensureTrailingNewline: (content) => {
    return content.trimEnd() + '\n';
  }
};

// Function to fix markdown linting issues based on common rules
function fixMarkdownLinting(content) {
  // MD012: No multiple consecutive blank lines
  content = content.replace(/\n{3,}/g, '\n\n');

  // MD009: Trailing spaces
  content = content.replace(/ +$/gm, '');

  // MD037: Spaces inside emphasis markers
  content = content.replace(/(\s)\*\*([^\s*](?:.*?[^\s*])?)\*\*(\s)/g, '$1**$2**$3'); // Avoid changing `** bold **`
  content = content.replace(/(\s)\*([^\s*](?:.*?[^\s*])?)\*(\s)/g, '$1*$2*$3');     // Avoid changing `* italic *`

  // MD038: Spaces inside code span elements
  content = content.replace(/`\s+([^`]+?)\s+`/g, '`$1`'); // ` code ` -> `code`
  content = content.replace(/`\s+([^`]+?)`/g, '`$1`');   // ` code` -> `code`
  content = content.replace(/`([^`]+?)\s+`/g, '`$1`');   // `code ` -> `code`

  // MD029: Ordered list item prefix (simple incrementing)
  let inOrderedList = false;
  let currentNumber = 1;
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const listMatch = line.match(/^(\s*)(\d+)\.\s+/);
    if (listMatch) {
      if (!inOrderedList) {
        inOrderedList = true;
        currentNumber = parseInt(listMatch[2]); // Start from the first number found
      }
      if (parseInt(listMatch[2]) !== currentNumber) {
        lines[i] = line.replace(/^(\s*)\d+\./, `$1${currentNumber}.`);
      }
      currentNumber++;
    } else if (line.trim() !== '' && !/^\s*$/.test(line)) { // Reset if not a blank line or whitespace only
      inOrderedList = false;
      currentNumber = 1;
    } else if (/^\s*$/.test(line) && inOrderedList) {
      // Blank line within a list - might reset numbering depending on indentation, simple approach resets
      inOrderedList = false;
      currentNumber = 1;
    }
  }
  content = lines.join('\n');


  // MD013: Line length - Add comment only, manual fix needed
  const hasLongLines = content.split('\n').some(line =>
    line.length > 100 && // Example length, adjust as needed
    !line.startsWith('http') &&
    !line.startsWith('`') &&
    !line.startsWith('|') && // Ignore table lines
    !line.startsWith('>') // Ignore blockquotes
  );
  if (hasLongLines && !content.startsWith('<!-- NOTE: MD013')) {
    content = `<!--
NOTE: This file may contain lines exceeding the recommended length (MD013).
Please consider breaking long lines for better readability.
-->\n\n${content}`;
  }

  return content;
}

// Process a file
function processFile(filePath) {
  console.log(`Processing ${filePath}`);
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let originalContent = content;

    // Apply common structural fixes first
    content = fixes.dashToAsterisk(content);
    content = fixes.fixListSpacing(content);
    content = fixes.blankLinesAroundLists(content);
    content = fixes.fixHeadings(content);
    content = fixes.fixCodeBlockBlankLines(content);

    // Apply linting rule fixes
    content = fixMarkdownLinting(content);

    // Ensure trailing newline last
    content = fixes.ensureTrailingNewline(content);

    // Write fixed content back only if changed
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`  Fixed and saved ${filePath}`);
    } else {
      console.log(`  No changes needed for ${filePath}`);
    }
  } catch (error) {
    console.error(`Error processing file ${filePath}: ${error}`);
  }
}

// Find all markdown files, excluding node_modules and .git
function findMarkdownFiles(dir, allFiles = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.resolve(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== 'node_modules' && entry.name !== '.git' && !entry.name.startsWith('.')) { // Added check for hidden dirs
        findMarkdownFiles(fullPath, allFiles);
      }
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      allFiles.push(fullPath);
    }
  }
  return allFiles;
}

// Main execution block
function main() {
  // Determine the root directory (assuming script is in 'scripts' or project root)
  let projectRoot = path.resolve(__dirname);
  if (path.basename(projectRoot) === 'scripts') {
    projectRoot = path.dirname(projectRoot);
  }
  console.log(`Project root identified as: ${projectRoot}`);

  const markdownFiles = findMarkdownFiles(projectRoot);
  console.log(`Found ${markdownFiles.length} Markdown files to process`);

  if (markdownFiles.length === 0) {
    console.log("No Markdown files found in the project directory.");
    return;
  }

  markdownFiles.forEach(processFile);
  console.log(`Processed ${markdownFiles.length} files`);

  // Specific handling for copilot-instructions.md if needed
  const copilotInstructionsPath = path.join(projectRoot, '.github', 'copilot-instructions.md');
  if (fs.existsSync(copilotInstructionsPath) && !markdownFiles.includes(copilotInstructionsPath)) {
    console.log("\nProcessing .github/copilot-instructions.md separately...");
    processFile(copilotInstructionsPath);
  } else if (fs.existsSync(copilotInstructionsPath)) {
    console.log("\n.github/copilot-instructions.md already processed.");
  } else {
    console.log("\n.github/copilot-instructions.md not found.");
  }
}

if (require.main === module) {
  main();
}
