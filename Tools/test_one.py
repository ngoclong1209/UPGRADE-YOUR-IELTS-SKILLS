import sys, os
sys.path.append('.')
from crawler.upgrade_all_tests import rebuild_files_for_test
rebuild_files_for_test('practicepteonline/listening/Test_1', 'listening', 1)
