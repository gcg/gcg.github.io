#!/bin/bash
set -e
grep -q "Guney Can Gokoglu" index.html || { echo "Missing owner name"; exit 1; }
grep -q "rotating-social-beacon" index.html || { echo "Missing beacon container"; exit 1; }
grep -q "Ubuntu" index.html || { echo "Missing Ubuntu in distro timeline"; exit 1; }
grep -q "Gentoo" index.html || { echo "Missing Gentoo in distro timeline"; exit 1; }
grep -q "Arch" index.html || { echo "Missing Arch in distro timeline"; exit 1; }
grep -q "Fedora" index.html || { echo "Missing Fedora in distro timeline"; exit 1; }
grep -q "Ruby on Rails" index.html || { echo "Missing Rails in language timeline"; exit 1; }
grep -q "Gleam" index.html || { echo "Missing Gleam in language timeline"; exit 1; }
grep -q "Poltio" index.html || { echo "Missing Poltio raid section"; exit 1; }
grep -q "mdwriter" index.html || { echo "Missing mdwriter artifact"; exit 1; }
grep -q "wpchanger" index.html || { echo "Missing wpchanger artifact"; exit 1; }
grep -q "AWS" index.html || { echo "Missing AWS in infra scope"; exit 1; }
grep -q "Google Cloud" index.html || { echo "Missing Google Cloud in infra scope"; exit 1; }
echo "Task 5 DOM markup verified"
