// tests/task3_rotating_id_test.js
const assert = require('assert');
const { getNextProfile, PROFILES } = require('../assets/js/rotating-id.js');

assert.strictEqual(PROFILES.length, 4, "Expected 4 profiles including Mastodon");
assert.deepStrictEqual(PROFILES.map(p => p.id), ['github', 'twitter', 'instagram', 'mastodon']);
assert.strictEqual(getNextProfile(0).id, 'twitter');
assert.strictEqual(getNextProfile(1).id, 'instagram');
assert.strictEqual(getNextProfile(2).id, 'mastodon');
assert.strictEqual(getNextProfile(3).id, 'github');
console.log("Task 3 rotating ID logic test passed (with Mastodon)");
