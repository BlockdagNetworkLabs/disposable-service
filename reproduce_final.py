
import sys
import os
sys.path.append('disposable')
from disposable import disposableHostGenerator
import logging

# Setup
TEST_OUT_FILE = 'test_domains_final'
TEST_DOMAIN_DNS = 'this-domain-definitely-does-not-exist-12345.com'
TEST_DOMAIN_WHITELIST = 'gmail.com'

# Create dummy old file
with open(f'{TEST_OUT_FILE}.txt', 'w') as f:
    f.write(f"{TEST_DOMAIN_DNS}\n{TEST_DOMAIN_WHITELIST}\n")

# Create dummy sha1 file
with open(f'{TEST_OUT_FILE}_sha1.txt', 'w') as f:
    f.write('somehash\n')

# Create dummy legacy file
with open(f'{TEST_OUT_FILE}_legacy.txt', 'w') as f:
    f.write(f"{TEST_DOMAIN_DNS}\n{TEST_DOMAIN_WHITELIST}\n")

print(f"Created {TEST_OUT_FILE}.txt with {TEST_DOMAIN_DNS} and {TEST_DOMAIN_WHITELIST}")

options = {
    'verbose': True,
    'skip_scrape': True,
    'src_filter': None,
    'skip_src': [],
    'whitelist': 'whitelist.txt', # Use real whitelist
    'dns_verify': True, # Enable DNS verify
    'dns_timeout': 2,
}

# Initialize
dhg = disposableHostGenerator(options, out_file=TEST_OUT_FILE)
dhg.sources = [] 

print("Running generate()...")
dhg.generate()

print(f"Domains after generate: {dhg.domains}")

success = True
if TEST_DOMAIN_DNS in dhg.domains:
    print("SUCCESS: Old domain preserved despite DNS failure.")
else:
    print("FAILURE: Old domain DELETED due to DNS failure.")
    success = False

if TEST_DOMAIN_WHITELIST in dhg.domains:
    print("SUCCESS: Old domain preserved despite whitelist.")
else:
    print("FAILURE: Old domain DELETED due to whitelist.")
    success = False

if success:
    print("ALL TESTS PASSED")
else:
    print("SOME TESTS FAILED")

# Cleanup
# os.remove(f'{TEST_OUT_FILE}.txt')
# os.remove(f'{TEST_OUT_FILE}_sha1.txt')
# os.remove(f'{TEST_OUT_FILE}_legacy.txt')
