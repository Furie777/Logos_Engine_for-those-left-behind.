#!/usr/bin/env node
/**
 * Self-Extracting Steganographic JavaScript
 *
 * This file looks like normal code but contains a hidden message
 * embedded in zero-width characters. Run it to extract the secret.
 */

const fs = require('fs');

// === VISIBLE CODE (looks completely normal) ===

function greet(name) {
  return `Hello, ${name}!`;
}

function add(a, b) {
  return a + b;
}

const utils = { greet, add, VERSION: '1.0.0' };

console.log(utils.greet('World'));
console.log('2 + 2 =', utils.add(2, 2));

// === HIDDEN EXTRACTION ===

const ZWC = {
  ZERO: '\u200B',
  ONE: '\u200C',
  SEP: '\u200D',
  BOUNDARY: '\uFEFF',
};

function extractHidden(text) {
  const start = text.indexOf(ZWC.BOUNDARY);
  const end = text.lastIndexOf(ZWC.BOUNDARY);
  if (start === -1 || end === -1 || start === end) return null;

  const hidden = text.slice(start + 1, end);
  const bytes = hidden.split(ZWC.SEP).filter(b => b.length > 0);

  let decoded = '';
  for (const byte of bytes) {
    let binary = '';
    for (const char of byte) {
      if (char === ZWC.ZERO) binary += '0';
      else if (char === ZWC.ONE) binary += '1';
    }
    if (binary.length === 8) {
      decoded += String.fromCharCode(parseInt(binary, 2));
    }
  }
  return decoded;
}

const self = fs.readFileSync(__filename, 'utf8');
const hidden = extractHidden(self);
if (hidden) {
  console.log('\n[SECRET EXTRACTED]:', hidden);
}

/* PAYLOAD: ﻿​‌​‌​‌​​‍​‌​​‌​​​‍​‌​​​‌​‌‍​‌​‌‌‌‌‌‍​‌​‌​‌​‌‍​‌​​‌‌‌​‍​‌​​‌​​‌‍​‌​‌​‌‌​‍​‌​​​‌​‌‍​‌​‌​​‌​‍​‌​‌​​‌‌‍​‌​​​‌​‌‍​‌​‌‌‌‌‌‍​‌​​‌​​‌‍​‌​‌​​‌‌‍​‌​‌‌‌‌‌‍​‌​​​​‌‌‍​‌​​‌​​​‍​‌​‌​‌​‌‍​‌​​‌‌‌​‍​‌​​‌​‌‌‍​‌​​​‌​‌‍​‌​​​‌​​‍﻿ */
