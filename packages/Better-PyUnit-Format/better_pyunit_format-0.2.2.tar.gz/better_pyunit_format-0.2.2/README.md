# Better PyUnit Format
#### A more readable text output for Python's built in unittest framework


### Overview

This package provides an implementation of a test runner and a test result for the Python unittest package.

This package simply creates an override of the built-in TextTestRunner that removes all the formatting that
it does by default and only runs the test suite. This means that this test runner passes all formatting
responsibility on to the test result. 

The test result that this package provides formats the output of the test in a much more readable way to make
interpreting unit test results a bit easier for introductory students.

This package is targeted towards students and education and was built with that limited use case in mind. 
With that said, please, feel free to use this in your applications and tell me what you think!

### Using Better PyUnit Format

1. Install the package via pip with `pip install Better-PyUnit-Format`
2. Import the `BetterPyUnitTestRunner`
3. Run your testsuite!


### Example code

```python
# run.py

import unittest
import test
from BetterPyUnitFormat import BetterPyUnitTestRunner

if __name__ == "__main__":
    testSuite = unittest.loader.makeSuite(test.Test)
    runner = BetterPyUnitTestRunner()
    runner.run(testSuite)

```

### Example Execution

```python
# test.py

import unittest


class Test(unittest.TestCase):
    def test_failure(self):
        """This test should fail"""
        self.assertEquals(1, 2)

    def test_success(self):
        """This test should pass"""
        self.assertEquals(1, 1)

    def test_error(self):
        """This test will error"""
        0/0

    @unittest.skip("Skipping this test :)")
    def test_skip(self):
        """This test will be skipped"""
        self.assertEquals(1, 2)
```
```text

====================
--------------------
[ RUN      ] This test will error (test.Test.test_error)
[    ERROR ] This test will error
A(n) ZeroDivisionError occurred:
[ZeroDivisionError] division by zero

-------------------- 

--------------------
[ RUN      ] This test should fail (test.Test.test_failure)
[     FAIL ] This test should fail
Failure reason:
1 != 2

-------------------- 

--------------------
[ RUN      ] This test will be skipped (test.Test.test_skip)
[     SKIP ] This test will be skipped
Skip Reason: Skipping this test :)
-------------------- 

--------------------
[ RUN      ] This test should pass (test.Test.test_success)
[       OK ] This test should pass
-------------------- 

====================
[  FAILED  ] 
1 tests passed.
1 tests failed.
1 tests errored.
1 tests skipped.
1 / 4
====================

```

### License
This package is licensed under the Unlicense. Feel free to use it for any purpose commercial or non-commercial.  
