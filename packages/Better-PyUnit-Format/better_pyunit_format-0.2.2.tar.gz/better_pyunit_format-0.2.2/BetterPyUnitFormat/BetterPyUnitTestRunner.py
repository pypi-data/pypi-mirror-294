from unittest import TextTestRunner
from unittest.signals import registerResult
from .BetterPyUnitResult import BetterPyUnitFormatResult


class BetterPyUnitTestRunner(TextTestRunner):
    def __init__(self, stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=BetterPyUnitFormatResult, warnings=None,
                 *, tb_locals=False):
        super().__init__(stream, descriptions, verbosity, failfast, buffer, resultclass, warnings, tb_locals=tb_locals)

    def run(self, test):
        """
        This function is adapted from the TextTestRunner in unittest.
        Basically, it is offloading all the result info to the results class and just serves as an actual runner.
        """
        result = super()._makeResult()
        registerResult(result)

        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals

        # these will always exist as part of the result class that we are using, but for compatibility we are keeping it
        startTestRun = getattr(result, 'startTestRun', None)
        stopTestRun = getattr(result, 'stopTestRun', None)

        if startTestRun is not None:
            startTestRun()

        try:
            test(result)
        finally:
            if stopTestRun is not None:
                stopTestRun()

        return result
