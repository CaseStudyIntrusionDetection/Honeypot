TANNER
======

<b><i>He who flays the hide</b></i>

About
-----
TANNER is a remote data analysis and classification service to evaluate HTTP requests and composing the response then served by SNARE.
TANNER uses multiple application vulnerability type emulation techniques when providing responses for SNARE. In addition,
TANNER provides Dorks for SNARE powering its luring capabilities.


Documentation
-------------
The documentation can be found [here](http://tanner.readthedocs.io).


Basic Concept
-------------

- Evaluating SNARE events.
- Serve dorks.
- Emulate vulnerabilities and provide responses.


Getting Started
---------------

- You need Python3.7 and above for installing tanner.
- This was tested with a recent Ubuntu-based Linux.

Testing
-------

In order to run the tests and receive a test coverage report, we recommend running `pytest`:

    pip install pytest pytest-cov
    sudo pytest --cov-report term-missing --cov=tanner tanner/tests/

Sample Output
-------------

```shell
    # sudo tanner

           _________    _   ___   ____________
          /_  __/   |  / | / / | / / ____/ __ \
           / / / /| | /  |/ /  |/ / __/ / /_/ /
          / / / ___ |/ /|  / /|  / /___/ _, _/
         /_/ /_/  |_/_/ |_/_/ |_/_____/_/ |_|


     Debug logs will be stored in /opt/tanner/tanner.log
     Error logs will be stored in /opt/tanner/tanner.err
     ======== Running on http://0.0.0.0:8090 ========
     (Press CTRL+C to quit)

```
