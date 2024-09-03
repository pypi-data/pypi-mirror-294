# ##################################################################################################
#  Copyright (c) 2023.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  If used, attribution of open-source code is included where required by original author          #
#                                                                                                  #
#  Filename:  retry.py                                                                             #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  retry.py                                                                             #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

#Copyright 2021 Fabian Bosler

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from functools import wraps
import time
import logging
import random
import os

logger = logging.getLogger(__name__)


def retry(exceptions, total_tries=6, initial_wait=0.1, backoff_factor=2.5, logger=None, no_print=False, fail_func=None):
    """
    calling the decorated function applying an exponential backoff.
    Args:
        exceptions: Exception(s) that trigger a retry, can be a tuple
        total_tries: Total tries
        initial_wait: Time to first retry
        backoff_factor: Backoff multiplier (e.g. value of 2 will double the delay each retry).
        logger: logger to be used, if none specified print
        no_print: Don't print retrying messages until ready to give up
    """
    def retry_decorator(f):
        @wraps(f)
        def func_with_retries(*args, **kwargs):
            _tries, _delay = total_tries + 1, initial_wait
            while _tries > 1:
                try:
                    if (total_tries + 2 - _tries) > 1 and not no_print:
                        log(f'<retry #{total_tries + 2 - _tries}>', logger)
                    return f(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    print_args = args if args else 'no args'
                    if _tries == 1:
                        if fail_func is not None:
                            try:
                                fail_func()
                            except Exception as e:
                                log(f'Retry: Failed to run fail_func: {e}', logger)
                            else:
                                log(f'Retry: fail_func ran successfully', logger)
                                time.sleep(10)
                                _tries = total_tries + 1 # reset tries
                                _delay = initial_wait  # reset delay
                                continue
                        msg = str(f'Function: {f.__name__}\n'
                                  f'Failed despite best efforts after {total_tries} tries.\n'
                                  f'args: {print_args}, kwargs: {kwargs}')
                        log(msg, logger)
                        raise
                    msg = str(f'Function: {f.__name__}\n'
                              f'Exception: {e}\n'
                              f'Retrying in {_delay}s args: {print_args}, kwargs: {kwargs}')
                    if not no_print:
                        log(msg, logger)
                    time.sleep(_delay)
                    _delay *= backoff_factor

        return func_with_retries
    return retry_decorator


def log(msg, logger=None):
    if logger:
        logger.warning(msg)
    else:
        print(msg)


def test_func(*args, **kwargs):
    rnd = random.random()
    if rnd < .2:
        raise ConnectionAbortedError('Connection was aborted :(')
    elif rnd < .4:
        raise ConnectionRefusedError('Connection was refused :/')
    elif rnd < .8:
        raise ConnectionResetError('Guess the connection was reset')
    else:
        return 'Yay!!'


# RQ addition.
@retry(FileNotFoundError, total_tries=7, initial_wait=0.5, backoff_factor=1.5)
def wait_on_file(file, pause=0):
    if pause:
        print(f'wait on file pause = {pause}')
        time.sleep(pause)
        pause = 0
    if not os.path.exists(file):
        raise FileNotFoundError(f"{file}")
    return True


if __name__ == '__main__':
    # wrapper = retry((ConnectionAbortedError), tries=3, delay=.2, backoff=1, logger=logger)
    # wrapped_test_func = wrapper(test_func)
    # print(wrapped_test_func('hi', 'bye', hi='ciao'))

    wrapper_all_exceptions = retry(Exception, total_tries=2, logger=logger)
    wrapped_test_func = wrapper_all_exceptions(test_func)
    print(wrapped_test_func('hi', 'bye', hi='ciao'))