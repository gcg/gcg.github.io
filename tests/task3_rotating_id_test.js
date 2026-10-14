// tests/task3_rotating_id_test.js
const assert = require('assert');
const { getNextProfile, PROFILES } = require('../assets/js/rotating-id.js');

assert.strictEqual(PROFILES.length, 3, "Expected 3 profiles");
assert.deepStrictEqual(PROFILES.map(p => p.id), ['github', 'twitter', 'instagram']);
assert.strictEqual(getNextProfile(0).id, 'twitter');
assert.strictEqual(getNextProfile(1).id, 'instagram');
assert.strictEqual(getNextProfile(2).id, 'github');
console.log("Task 3 rotating ID logic test passed");
