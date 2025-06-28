import sys

from tests import test_v38

if __name__ == "__main__":
    is_fail_fast = "--fail-fast" in sys.argv

    if not test_v38.test_batch("tests/v38") and is_fail_fast:
        sys.exit(1)
