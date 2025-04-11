#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Function to fix broken links in markdown content
function fixBrokenLinks(content) {
  // Replace the broken link to /workspaces/--ThinkAlike--/.github/link
  content = content.replace(/\(\/workspaces\/--ThinkAlike--\/.github\/link\)/g, '(https://github.com/EosLumina/--ThinkAlike--)');

  return content;
}

// Fix the copilot-instructions.md file
const filePath = '/workspaces/--ThinkAlike--/.github/copilot-instructions.md';
console.log(`Fixing broken links in ${filePath}`);
const content = fs.readFileSync(filePath, 'utf8');
const fixedContent = fixBrokenLinks(content);
fs.writeFileSync(filePath, fixedContent);
console.log('Fixed broken links in copilot-instructions.md');
