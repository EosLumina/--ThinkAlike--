#!/usr/bin/env node

/**
 * ThinkAlike Markdown Visual Issue Fixer
 *
 * This script specifically targets visual formatting issues in markdown files
 * that cause display problems in GitHub and other markdown renderers.
 *
 * Features:
 * - Fixes list indentation and bullet formatting
 * - Normalizes badges and URLs for proper display
 * - Properly formats headings and emphasis markers
 * - Ensures proper spacing around block elements
 * - Fixes common GitHub markdown rendering quirks
 * - Handles special cases for README.md and documentation files
 *
 * Usage: node scripts/fix-markdown-visual-issues.js [filepath]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('📝 ThinkAlike Markdown Visual Issue Fixer 📝');
console.log('-------------------------------------------');

// Process a single file
function processFile(filePath) {
  try {
    console.log(`Processing: ${filePath}`);
    const content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;

    // Apply specialized fixes
    let fixedContent = fixVisualIssues(content, path.basename(filePath));

    // Write changes back if content was modified
    if (fixedContent !== originalContent) {
      fs.writeFileSync(filePath, fixedContent);
      console.log(`✅ Fixed visual issues in: ${filePath}`);
      return true;
    } else {
      console.log(`❓ No visual issues identified in: ${filePath}`);
      return false;
    }
  } catch (error) {
    console.error(`❌ Error processing ${filePath}: ${error.message}`);
    return false;
  }
}

// Main fix function with special handling for different file types
function fixVisualIssues(content, filename) {
  // Apply common fixes
  let result = content;

  // Fix list items with asterisks
  result = fixListItems(result);

  // Fix badge formatting (especially in README.md)
  result = fixBadgeFormatting(result);

  // Fix heading formatting
  result = fixHeadings(result);

  // Fix emphasis markers
  result = fixEmphasisMarkers(result);

  // Fix URLs
  result = fixUrls(result);

  // Fix horizontal rules
  result = fixHorizontalRules(result);

  // Special fixes for README.md
  if (filename === 'README.md') {
    result = fixReadmeSpecific(result);
  }

  // Special fixes for user guides
  if (filename.includes('_guide') || filename.includes('user_stories')) {
    result = fixDocumentationSpecific(result);
  }

  return result;
}

// Fix list items formatting
function fixListItems(content) {
  let result = content;

  // Fix asterisk list items ensuring proper spacing
  result = result.replace(/^(\s*)\*(\s*)([^\s*])/gm, '$1* $3');

  // Fix hyphen list items
  result = result.replace(/^(\s*)-(\s*)([^\s-])/gm, '$1* $3');

  // Fix plus list items
  result = result.replace(/^(\s*)\+(\s*)([^\s+])/gm, '$1* $3');

  // Fix numbered list items
  result = result.replace(/^(\s*)(\d+)\.(\s*)([^\s])/gm, '$1$2. $4');

  // Ensure proper spacing before and after lists
  result = result.replace(/([^\n])\n(\s*[*+-]|\s*\d+\.)/g, '$1\n\n$2');
  result = result.replace(/^(\s*[*+-].*|s*\d+\..*)\n([^\s*+-\d])/gm, '$1\n\n$2');

  // Fix nested list indentation
  result = result.replace(/^( {1,3})[*+-]/gm, '  *');
  result = result.replace(/^(  {1,3})[*+-]/gm, '    *');

  return result;
}

// Fix badge formatting for README
function fixBadgeFormatting(content) {
  let result = content;

  // Fix broken badge links (common in README.md)
  result = result.replace(/\[!\[([^\]]+)\]\(([^)]+)\)\]\(([^)]+)\)/g, '[![$1]($2)]($3)');

  // Fix badge spacing issues
  result = result.replace(/(\]\([^)]+\))(\[!\[)/g, '$1\n$2');

  // Fix badge URLs that got split across lines
  result = result.replace(/\]\(([^\n)]*)\n([^)]*)\)/g, ']($1$2)');

  return result;
}

// Fix headings format
function fixHeadings(content) {
  let result = content;

  // Ensure space after # in headings
  result = result.replace(/^(#+)([^ #])/gm, '$1 $2');

  // Ensure blank lines before headings
  result = result.replace(/([^\n])(\n#+\s)/g, '$1\n\n$2');

  // Ensure blank lines after headings
  result = result.replace(/^(#+\s.*)\n([^#\n])/gm, '$1\n\n$2');

  // Fix heading levels (no skipping levels)
  result = result.replace(/^######\s/gm, '###### ');
  result = result.replace(/^#####\s/gm, '##### ');
  result = result.replace(/^####\s/gm, '#### ');
  result = result.replace(/^###\s/gm, '### ');
  result = result.replace(/^##\s/gm, '## ');
  result = result.replace(/^#\s/gm, '# ');

  return result;
}

// Fix emphasis markers
function fixEmphasisMarkers(content) {
  let result = content;

  // Standardize strong emphasis to asterisks
  result = result.replace(/__([^_]+)__/g, '**$1**');

  // Fix emphasis with spaces
  result = result.replace(/\*\*(\s+)([^*]+)(\s+)\*\*/g, ' **$2** ');

  // Fix broken emphasis across lines
  result = result.replace(/\*\*([^\n*]*)\n([^*]*)\*\*/g, '**$1 $2**');

  return result;
}

// Fix URL formatting
function fixUrls(content) {
  let result = content;

  // Fix bare URLs by adding angle brackets
  result = result.replace(/(?<![(<`])(https?:\/\/[^\s"]+)(?![)>\s`])/g, '<$1>');

  // Fix broken URLs that got split across lines
  result = result.replace(/\[([^\]]+)\]\(([^\n)]*)\n([^)]*)\)/g, '[$1]($2$3)');

  // Fix URLs with spaces
  result = result.replace(/\[([^\]]+)\]\(\s+([^)\s]+)\s+\)/g, '[$1]($2)');

  return result;
}

// Fix horizontal rules
function fixHorizontalRules(content) {
  let result = content;

  // Standardize horizontal rules
  result = result.replace(/^(\s*)-{3,}\s*$/gm, '$1* --');
  result = result.replace(/^(\s*)\*{3,}\s*$/gm, '$1* --');
  result = result.replace(/^(\s*)_{3,}\s*$/gm, '$1* --');

  // Ensure proper spacing around horizontal rules
  result = result.replace(/([^\n])\n(\s*\* --)/g, '$1\n\n$2');
  result = result.replace(/^(\s*\* --)\n([^\n])/gm, '$1\n\n$2');

  return result;
}

// Fix README-specific issues
function fixReadmeSpecific(content) {
  let result = content;

  // Fix badge alignment
  result = result.replace(/^(!\[.+?\]\(.+?\))\s*(!\[.+?\]\(.+?\))/gm, '$1\n$2');

  // Ensure proper spacing in feature lists
  result = result.replace(/^(\s*)\*\s+\*\*(.+?)\*\*:/gm, '$1* **$2**:');

  // Fix special sections like licenses
  result = result.replace(/^(#+\s+License)$/gm, '\n$1');

  return result;
}

// Fix documentation-specific issues
function fixDocumentationSpecific(content) {
  let result = content;

  // Fix document details formatting
  result = result.replace(/^(\*\s+Title:.*)/gm, '* **Title:**$1');
  result = result.replace(/^(\*\s+Type:.*)/gm, '* **Type:**$1');
  result = result.replace(/^(\*\s+Version:.*)/gm, '* **Version:**$1');

  // Fix story formatting in user stories documents
  result = result.replace(/^(\s*\*\*[^*]+\*\*):/gm, '$1:');

  // Fix numbered sections
  result = result.replace(/^(\d+\.\s+)([A-Z])/gm, '## $1$2');

  return result;
}

// Process files based on arguments
function processMarkdownFiles() {
  const specifiedFile = process.argv[2];

  try {
    if (specifiedFile) {
      // Process only the specified file
      console.log(`Processing single file: ${specifiedFile}`);
      processFile(specifiedFile);
    } else {
      // Process a set of visually problematic files
      const criticalFiles = [
        '/workspaces/--ThinkAlike--/README.md',
        '/workspaces/--ThinkAlike--/docs/guides/user_guides/mode2_discovery_guide.md',
        '/workspaces/--ThinkAlike--/docs/use_cases/user_stories_narrative_mode.md',
        '/workspaces/--ThinkAlike--/docs/use_cases/user_stories_matching_mode.md',
        '/workspaces/--ThinkAlike--/docs/vision/vision_concepts.md',
        '/workspaces/--ThinkAlike--/docs/vision/core_concepts.md'
      ];

      console.log(`Processing ${criticalFiles.length} visually problematic files...`);

      let fixedCount = 0;
      criticalFiles.forEach(file => {
        if (fs.existsSync(file)) {
          if (processFile(file)) {
            fixedCount++;
          }
        } else {
          console.log(`⚠️ File not found: ${file}`);
        }
      });

      console.log(`\n✨ Process complete! Fixed visual issues in ${fixedCount}/${criticalFiles.length} files.`);
    }
  } catch (error) {
    console.error(`Failed to process files: ${error.message}`);
    process.exit(1);
  }
}

// Run the processing function
processMarkdownFiles();
