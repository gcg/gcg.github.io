// tests/task4_hunter_fx_test.js
const assert = require('assert');
const { formatStatValue } = require('../assets/js/hunter-fx.js');

assert.strictEqual(formatStatValue(23, 'int'), '23');
assert.strictEqual(formatStatValue(99.999, 'percent'), '99.999%');
assert.strictEqual(formatStatValue(12, 'int'), '12');
console.log("Task 4 hunter-fx logic test passed");
