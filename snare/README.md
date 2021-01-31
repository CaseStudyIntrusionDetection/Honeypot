SNARE
=====

_**Super Next generation Advanced Reactive honEypot**_

About
-----

SNARE is a web application honeypot sensor attracting all sort of maliciousness from the Internet.

Documentation
--------------

The documentation can be found [here](http://snare.readthedocs.io).

Basic Concepts
--------------

- Surface first. Focus on the attack surface generation.
- Sensors and masters. Lightweight collectors (SNARE) and central decision maker (tanner).

## Testing

In order to run the tests and receive a test coverage report, we recommend running `pytest`:

```
    pip install pytest pytest-cov
    sudo pytest --cov-report term-missing --cov=snare snare/tests/
```

## Sample Output

```shell

    # sudo snare --port 8080 --page-location example.com

       _____ _   _____    ____  ______
      / ___// | / /   |  / __ \/ ____/
      \__ \/  |/ / /| | / /_/ / __/
     ___/ / /|  / ___ |/ _, _/ /___
    /____/_/ |_/_/  |_/_/ |_/_____/


    privileges dropped, running as "nobody:nogroup"
    serving with uuid 9c10172f-7ce2-4fb4-b1c6-abc70141db56
    Debug logs will be stored in /opt/snare/snare.log
    Error logs will be stored in /opt/snare/snare.err
    ======== Running on http://127.0.0.1:8080 ========
    (Press CTRL+C to quit)
    you are running the latest version

```