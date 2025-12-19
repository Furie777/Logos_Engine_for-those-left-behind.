#!/bin/bash
0<0// /*
echo "Executed by Bash!"
exit 0
#*/ void 0;

// Hidden payload in comment: ﻿​‌​‌​​‌‌‍​‌​​​‌​‌‍​‌​​​​‌‌‍​‌​‌​​‌​‍​‌​​​‌​‌‍​‌​‌​‌​​‍​‌​‌‌‌‌‌‍​‌​​​‌​​‍​‌​‌​‌​‌‍​‌​​​​​‌‍​‌​​‌‌​​‍​‌​‌‌‌‌‌‍​‌​​​‌​‌‍​‌​‌‌​​​‍​‌​​​‌​‌‍​‌​​​​‌‌‍﻿
// Node.js code:
console.log('Executed by Node!');
const { decode } = require('./zwc-stego');
const fs = require('fs');
const self = fs.readFileSync(__filename, 'utf8');
const hidden = decode(self);
console.log('Hidden message found:', hidden);
