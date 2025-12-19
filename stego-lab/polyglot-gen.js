#!/usr/bin/env node
/**
 * Polyglot File Generator with Zero-Width Steganography
 *
 * Creates files that are simultaneously valid as multiple formats,
 * while also containing hidden zero-width encoded messages.
 *
 * Polyglot types:
 *   1. HTML + JavaScript - renders in browser, executes in Node
 *   2. Markdown + HTML + hidden message
 *   3. Shell script + JavaScript
 */

const fs = require('fs');
const { encode, reveal, analyze } = require('./zwc-stego');

/**
 * Creates an HTML/JavaScript polyglot with hidden message
 * - Opens in browser: renders HTML content
 * - Runs with Node: executes JavaScript
 * - Contains invisible zero-width encoded secret
 */
function createHtmlJsPolyglot(htmlContent, jsCode, secretMessage) {
  // The trick: HTML ignores script content until </script>
  // Node ignores HTML comments
  // Zero-width chars are invisible in both

  const hiddenPayload = secretMessage ? encode('', secretMessage) : '';

  const polyglot = `<!--${hiddenPayload}
/* HTML sees this as a comment, JS sees it as a block comment starting here */
//--><!DOCTYPE html>
<html>
<head><title>Normal Page</title></head>
<body>
${htmlContent}
<script>
/* This runs in browser */
document.body.innerHTML += '<p style="color:green">JavaScript executed in browser!</p>';
</script>
<!--
//-->
<script>/* Hide JS from browser with type *///</script>
<!--
${jsCode}
//-->
</body>
</html>
<!--
/* Node.js execution starts here */
${jsCode}
//-->`;

  return polyglot;
}

/**
 * Creates a Markdown file with hidden message
 * - Renders as normal Markdown
 * - Contains invisible steganographic payload
 * - Also valid HTML
 */
function createMarkdownPolyglot(markdownContent, secretMessage) {
  // Hide the secret in what looks like an empty line
  const hiddenLine = encode('', secretMessage);

  const polyglot = `${markdownContent}
${hiddenLine}
<!-- This is valid HTML comment, invisible in Markdown -->
<div style="display:none">
Hidden HTML content that Markdown renderers may ignore
</div>
`;

  return polyglot;
}

/**
 * Creates a shell/Node polyglot with hidden message
 * - Runs with bash: executes shell commands
 * - Runs with node: executes JavaScript
 * - Contains zero-width hidden message
 */
function createShellNodePolyglot(shellCommand, jsCode, secretMessage) {
  const hiddenPayload = secretMessage ? encode('', secretMessage) : '';

  // Polyglot trick:
  // - Line 1: shebang for bash
  // - Line 2: 0<0// is falsy redirect in bash (no-op), starts JS comment
  // - Hidden payload in bash heredoc that JS sees as template literal
  const polyglot = `#!/bin/bash
0<0// /*
${shellCommand}
exit 0
#*/ void 0;

// Hidden payload in comment: ${hiddenPayload}
// Node.js code:
${jsCode}
`;

  return polyglot;
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'html-js') {
    const secret = args[1] || 'SECRET_PAYLOAD';
    const html = '<h1>Welcome to a Normal Webpage</h1><p>Nothing suspicious here.</p>';
    const js = `console.log('Node.js executed! Secret was: ${secret}');`;

    const polyglot = createHtmlJsPolyglot(html, js, secret);

    fs.writeFileSync('polyglot.html', polyglot);
    console.log('\n=== CREATED: polyglot.html ===');
    console.log('- Open in browser: renders HTML');
    console.log('- Run with Node: executes JS');
    console.log('- Contains hidden message:', secret);
    console.log('\nAnalysis:', analyze(polyglot));
    console.log('\nTest it:');
    console.log('  node polyglot.html');
    console.log('  # or open in browser');

  } else if (command === 'markdown') {
    const secret = args[1] || 'HIDDEN_IN_MARKDOWN';
    const md = `# Innocent README

This is a normal markdown file. Nothing to see here.

## Features

- Looks completely normal
- Renders in any Markdown viewer
- Contains **zero** suspicious content

## License

MIT
`;

    const polyglot = createMarkdownPolyglot(md, secret);

    fs.writeFileSync('polyglot.md', polyglot);
    console.log('\n=== CREATED: polyglot.md ===');
    console.log('- Renders as normal Markdown');
    console.log('- Contains hidden message:', secret);
    console.log('\nAnalysis:', analyze(polyglot));

  } else if (command === 'shell-node') {
    const secret = args[1] || 'DUAL_EXECUTION';
    const shell = 'echo "Executed by Bash!"';
    const js = `console.log('Executed by Node!');
const { decode } = require('./zwc-stego');
const fs = require('fs');
const self = fs.readFileSync(__filename, 'utf8');
const hidden = decode(self);
console.log('Hidden message found:', hidden);`;

    const polyglot = createShellNodePolyglot(shell, js, secret);

    fs.writeFileSync('polyglot.sh', polyglot);
    fs.chmodSync('polyglot.sh', '755');
    console.log('\n=== CREATED: polyglot.sh ===');
    console.log('- Run with bash: ./polyglot.sh');
    console.log('- Run with node: node polyglot.sh');
    console.log('- Contains hidden message:', secret);
    console.log('\nAnalysis:', analyze(polyglot));

  } else if (command === 'demo') {
    console.log('\n=== POLYGLOT + STEGANOGRAPHY DEMO ===\n');

    // Create all three types
    const secret = 'THE_TRUTH_IS_HIDDEN';

    // HTML/JS polyglot
    const htmlJs = createHtmlJsPolyglot(
      '<h1>Normal Page</h1>',
      `console.log('Secret extracted!');`,
      secret
    );
    fs.writeFileSync('demo-polyglot.html', htmlJs);

    // Markdown polyglot
    const md = createMarkdownPolyglot('# Normal README\n\nJust a readme.', secret);
    fs.writeFileSync('demo-polyglot.md', md);

    console.log('Created demo files with hidden message:', secret);
    console.log('\nFiles created:');
    console.log('  demo-polyglot.html - HTML + JS + hidden message');
    console.log('  demo-polyglot.md   - Markdown + hidden message');
    console.log('\nTo extract hidden message:');
    console.log('  node zwc-stego.js decode "$(cat demo-polyglot.md)"');

  } else {
    console.log(`
Polyglot Generator with Steganography

Usage:
  node polyglot-gen.js html-js [secret]     Create HTML/JS polyglot
  node polyglot-gen.js markdown [secret]    Create Markdown polyglot
  node polyglot-gen.js shell-node [secret]  Create Shell/Node polyglot
  node polyglot-gen.js demo                 Create demo files

Examples:
  node polyglot-gen.js html-js "TOP_SECRET"
  node polyglot-gen.js markdown "HIDDEN_DATA"
    `);
  }
}

module.exports = { createHtmlJsPolyglot, createMarkdownPolyglot, createShellNodePolyglot };
