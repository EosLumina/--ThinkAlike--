// filepath: scripts/fix-markdown-linting.js
const fs = require('fs');
const path = require('path');
const glob = require('glob');
const chalk = require('chalk');

// Configuration
const config = {
  lineLength: 100,           // Maximum line length
  standardListMarker: '*',   // Preferred list marker (* or -)
  orderedListStyle: '1.',    // Style for ordered lists
};

function fixMarkdownFile(filePath) {
  console.log(chalk.blue(`Processing ${filePath}...`));
  let content = fs.readFileSync(filePath, 'utf8');
  let fixed = false;

  // Fix line length (MD013)
  const longLines = content.split('\n').filter(line =>
    line.length > config.lineLength &&
    !line.startsWith('```') &&
    !line.startsWith('http')
  );

  if (longLines.length > 0) {
    // We're not actually wrapping lines here as it's complex
    // Just reporting them for manual review
    console.log(chalk.yellow(`  Found ${longLines.length} lines exceeding ${config.lineLength} characters`));
    fixed = true;
  }

  // Fix missing blank lines around headings (MD022)
  const newContent = content.replace(/^(#+\s+.+?)$\n([^\n])/gm, '$1\n\n$2');
  if (newContent !== content) {
    content = newContent;
    console.log(chalk.green('  Fixed missing blank lines after headings'));
    fixed = true;
  }

  // Standardize list markers (MD004)
  const listMarkers = content.match(/^[ \t]*[-*+][ \t]+/gm);
  if (listMarkers && listMarkers.some(marker => !marker.includes(config.standardListMarker))) {
    // Replace all list markers with the standard one
    const standardized = content.replace(/^([ \t]*)[-*+]([ \t]+)/gm, `$1${config.standardListMarker}$2`);
    if (standardized !== content) {
      content = standardized;
      console.log(chalk.green(`  Standardized list markers to ${config.standardListMarker}`));
      fixed = true;
    }
  }

  // Fix multiple consecutive blank lines (MD012)
  const multipleBlankLines = content.replace(/\n{3,}/g, '\n\n');
  if (multipleBlankLines !== content) {
    content = multipleBlankLines;
    console.log(chalk.green('  Fixed multiple consecutive blank lines'));
    fixed = true;
  }

  // Fix ordered list numbering (MD029)
  // This is a simple approach - for more complex lists, a full parser would be needed
  let inOrderedList = false;
  let currentNumber = 1;
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const listMatch = line.match(/^([ \t]*)(\d+)\.[ \t]/);

    if (listMatch) {
      if (!inOrderedList) {
        inOrderedList = true;
        currentNumber = 1;
      }

      if (parseInt(listMatch[2]) !== currentNumber) {
        lines[i] = line.replace(/^([ \t]*)\d+\./, `$1${currentNumber}.`);
        fixed = true;
      }

      currentNumber++;
    } else if (line.trim() === '') {
      inOrderedList = false;
    }
  }

  content = lines.join('\n');

  // Handle document details sections consistently
  // Look for patterns like "**Document Details**" and format them consistently
  const docDetailsPattern = /\*\*Document Details\*\*\s*\n/g;
  if (content.match(docDetailsPattern)) {
    // Format is found, we could standardize it here
    console.log(chalk.blue('  Document details section found - ensure consistent formatting'));
  }

  // Save changes if we fixed anything
  if (fixed) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(chalk.green('  Saved changes'));
  } else {
    console.log(chalk.gray('  No issues to fix'));
  }

  return fixed;
}

function fixAllMarkdownFiles() {
  // Find all markdown files in the docs directory
  // Adjust the glob pattern if your markdown files are elsewhere
  const files = glob.sync('docs/**/*.md', { cwd: path.resolve(__dirname, '..') }); // Ensure glob runs from project root

  console.log(chalk.blue(`Found ${files.length} markdown files to process`));

  let fixedCount = 0;

  for (const file of files) {
    // Construct the full path relative to the script's execution context
    const fullPath = path.resolve(__dirname, '..', file);
    if (fixMarkdownFile(fullPath)) {
      fixedCount++;
    }
  }

  console.log(chalk.green(`Fixed issues in ${fixedCount} out of ${files.length} files`));
}

// Execute the function if the script is run directly
if (require.main === module) {
  fixAllMarkdownFiles();
}

module.exports = {
  fixMarkdownFile,
  fixAllMarkdownFiles
};
