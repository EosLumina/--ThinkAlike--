#!/usr/bin/env node

/**
 * Markdown Lint Fixer
 *
 * This script automatically fixes common markdown linting issues in ThinkAlike documentation.
 * It addresses:
 * - List formatting (MD032, MD007)
 * - Code block language specification (MD040)
 * - Heading formatting (MD025, MD026)
 *
 * Usage:
 *   node scripts/fix-markdown-linting.js path/to/file.md
 *   node scripts/fix-markdown-linting.js --all  # Process all markdown files
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function fixMarkdownFile(filePath) {
  console.log(`Processing: ${filePath}`);

  try {
    // Read file content
    let content = fs.readFileSync(filePath, 'utf8');

    // Fix lists not surrounded by blank lines (MD032)
    content = content.replace(/^([^\n])([-*+] )/gm, '$1\n\n$2');
    content = content.replace(/([-*+] [^\n]+)([^\n])/gm, '$1\n\n$2');

    // Fix list indentation (MD007) - Make all lists use 2 space indentation
    content = content.replace(/^( {0,1})([-*+] )/gm, '  $2');

    // Fix unordered list style (MD004) - Use dashes for all lists
    content = content.replace(/^( *)[*+]( )/gm, '$1-$2');

    // Fix fenced code blocks without language (MD040)
    content = content.replace(/^```\s*$/gm, '```text');

    // Fix multiple top-level headings (MD025)
    // First find the first h1, then replace subsequent h1s with h2s
    const lines = content.split('\n');
    let foundFirstH1 = false;
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].startsWith('# ')) {
        if (foundFirstH1) {
          // Change subsequent h1s to h2s
          lines[i] = '## ' + lines[i].substring(2);
        } else {
          foundFirstH1 = true;
        }
      }
    }
    content = lines.join('\n');

    // Fix bare URLs (MD034)
    content = content.replace(/(?<![(`])(https?:\/\/[^\s)>]+)(?![)`])/g, '<$1>');

    // Fix trailing punctuation in heading (MD026)
    content = content.replace(/^(#+.*[:.!?])$/gm, (match) => {
      return match.substring(0, match.length - 1);
    });

    // Fix headings not surrounded by blank lines (MD022, MD023)
    content = content.replace(/^([^\n])((#{1,6}) )/gm, '$1\n\n$2');
    content = content.replace(/^((#{1,6}) [^\n]+)([^\n])/gm, '$1\n\n$3');

    // Fix fenced code blocks not surrounded by blank lines (MD031)
    content = content.replace(/^([^\n])(```)/gm, '$1\n\n$2');
    content = content.replace(/(```)([^\n])/gm, '$1\n\n$2');

    // Write back fixed content
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✅ Fixed linting issues in: ${filePath}`);
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error);
  }
}

function processAllMarkdownFiles() {
  // Find all markdown files in the project
  try {
    const result = execSync('find /workspaces/--ThinkAlike-- -type f -name "*.md"', { encoding: 'utf8' });
    const files = result.trim().split('\n');

    console.log(`Found ${files.length} markdown files`);
    files.forEach(file => fixMarkdownFile(file));

    console.log('✅ Completed fixing markdown linting issues');
  } catch (error) {
    console.error('❌ Error finding markdown files:', error);
  }
}

// Process command line arguments
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Usage:');
  console.log('  node scripts/fix-markdown-linting.js path/to/file.md');
  console.log('  node scripts/fix-markdown-linting.js --all  # Process all markdown files');
} else if (args[0] === '--all') {
  processAllMarkdownFiles();
} else {
  fixMarkdownFile(args[0]);
}

#!/usr/bin/env node

/**
 * Script to fix README.md badges and other markdown issues
 */

// Get the file path from command line arguments
const filePath = process.argv[2];

if (!filePath) {
  console.error('Please provide a file path argument');
  process.exit(1);
}

// Read the file
try {
  let content = fs.readFileSync(filePath, 'utf8');

  // Fix common badge issues
  content = content
    // Fix workflow badge links
    .replace(/https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/actions\/workflows\/([^\/]+)\/badge\.svg/g,
             'https://github.com/EosLumina/--ThinkAlike--/actions/workflows/$3/badge.svg')

    // Fix repository references
    .replace(/github\.com\/([^\/]+)\/ThinkAlike/g,
             'github.com/EosLumina/--ThinkAlike--')

    // Fix other common markdown issues
    .replace(/\r\n/g, '\n')                // Normalize line endings
    .replace(/\n{3,}/g, '\n\n')           // Remove extra blank lines
    .replace(/\*\s+\*/g, '*')             // Fix broken lists
    .replace(/\[\]\((?!http)[^\)]+\)/g, match => {
      // Fix relative links
      const urlPart = match.match(/\[\]\((.*)\)/)[1];
      if (urlPart.startsWith('/')) {
        return match;
      } else if (urlPart.startsWith('./')) {
        return match;
      } else {
        return match.replace(/\[\]\((.*)\)/, '[](./$1)');
      }
    });

  // Write the fixed content back to the file
  fs.writeFileSync(filePath, content);
  console.log(`Successfully fixed issues in ${filePath}`);
} catch (err) {
  console.error(`Error processing ${filePath}:`, err);
  process.exit(1);
}
