#!/usr/bin/env node
/**
 * Zero-Width Character Steganography
 *
 * Hides secret messages inside normal-looking text using invisible Unicode characters.
 * The carrier text looks completely normal, but contains hidden data.
 *
 * Zero-width characters used:
 *   U+200B (ZERO WIDTH SPACE)      = binary 0
 *   U+200C (ZERO WIDTH NON-JOINER) = binary 1
 *   U+200D (ZERO WIDTH JOINER)     = byte separator
 *   U+FEFF (BOM)                   = message boundary
 */

const ZWC = {
  ZERO: '\u200B',      // Binary 0
  ONE: '\u200C',       // Binary 1
  SEP: '\u200D',       // Byte separator
  BOUNDARY: '\uFEFF',  // Start/end of hidden message
};

// Encode a string to binary, then to zero-width characters
function textToZWC(secret) {
  let zwcString = ZWC.BOUNDARY;

  for (const char of secret) {
    const binary = char.charCodeAt(0).toString(2).padStart(8, '0');
    for (const bit of binary) {
      zwcString += bit === '0' ? ZWC.ZERO : ZWC.ONE;
    }
    zwcString += ZWC.SEP;
  }

  zwcString += ZWC.BOUNDARY;
  return zwcString;
}

// Decode zero-width characters back to text
function zwcToText(zwcString) {
  // Find content between boundaries
  const start = zwcString.indexOf(ZWC.BOUNDARY);
  const end = zwcString.lastIndexOf(ZWC.BOUNDARY);

  if (start === -1 || end === -1 || start === end) {
    return null; // No hidden message found
  }

  const hidden = zwcString.slice(start + 1, end);
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

// Hide a secret message inside carrier text
function encode(carrierText, secretMessage) {
  const zwcPayload = textToZWC(secretMessage);
  // Insert the invisible payload after the first word
  const firstSpace = carrierText.indexOf(' ');
  if (firstSpace === -1) {
    return carrierText + zwcPayload;
  }
  return carrierText.slice(0, firstSpace) + zwcPayload + carrierText.slice(firstSpace);
}

// Extract hidden message from text
function decode(stegoText) {
  return zwcToText(stegoText);
}

// Reveal hidden characters visually (for debugging)
function reveal(text) {
  return text
    .replace(/\u200B/g, '[0]')
    .replace(/\u200C/g, '[1]')
    .replace(/\u200D/g, '[SEP]')
    .replace(/\uFEFF/g, '[BND]');
}

// Stats about hidden content
function analyze(text) {
  const counts = {
    zero: (text.match(/\u200B/g) || []).length,
    one: (text.match(/\u200C/g) || []).length,
    sep: (text.match(/\u200D/g) || []).length,
    boundary: (text.match(/\uFEFF/g) || []).length,
  };
  counts.totalHidden = counts.zero + counts.one + counts.sep + counts.boundary;
  counts.hiddenBytes = Math.floor((counts.zero + counts.one) / 8);
  counts.visibleLength = text.replace(/[\u200B\u200C\u200D\uFEFF]/g, '').length;
  return counts;
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'encode' && args.length >= 3) {
    const carrier = args[1];
    const secret = args.slice(2).join(' ');
    const result = encode(carrier, secret);
    console.log('\n=== ENCODED ===');
    console.log(result);
    console.log('\n=== ANALYSIS ===');
    console.log(analyze(result));
    console.log('\n=== REVEALED (debug) ===');
    console.log(reveal(result));

  } else if (command === 'decode' && args.length >= 2) {
    const stego = args.slice(1).join(' ');
    const secret = decode(stego);
    console.log('\n=== DECODED ===');
    console.log(secret || '(no hidden message found)');

  } else if (command === 'analyze' && args.length >= 2) {
    const text = args.slice(1).join(' ');
    console.log('\n=== ANALYSIS ===');
    console.log(analyze(text));

  } else if (command === 'demo') {
    console.log('\n=== ZERO-WIDTH STEGANOGRAPHY DEMO ===\n');

    const carrier = "This is a completely normal sentence.";
    const secret = "HIDDEN";

    console.log('Carrier text:', carrier);
    console.log('Secret message:', secret);

    const encoded = encode(carrier, secret);
    console.log('\nEncoded (looks identical):');
    console.log(encoded);

    console.log('\nRevealed structure:');
    console.log(reveal(encoded));

    console.log('\nAnalysis:', analyze(encoded));

    console.log('\nDecoded secret:', decode(encoded));

    console.log('\n=== THE TEXT LOOKS NORMAL BUT CONTAINS SECRETS ===');

  } else {
    console.log(`
Zero-Width Character Steganography

Usage:
  node zwc-stego.js encode <carrier> <secret>   Hide secret in carrier text
  node zwc-stego.js decode <stego-text>         Extract hidden message
  node zwc-stego.js analyze <text>              Analyze for hidden content
  node zwc-stego.js demo                        Run demonstration
    `);
  }
}

module.exports = { encode, decode, reveal, analyze, textToZWC, zwcToText };
