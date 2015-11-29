import os
import signal
import subprocess
import time

import pytest

SELENIUM_PATH = os.getenv(
    "SELENIUM_PATH",
    os.path.join(
        os.path.expanduser("~"),
        "selenium-server-standalone-2.28.0.jar"
    )
)


@pytest.fixture(scope="session")
def selenium(request):
    pid = subprocess.Popen(["java", "-jar", SELENIUM_PATH]).pid
    time.sleep(3)

    def fin():
        os.kill(pid, signal.SIGTERM)

    request.addfinalizer(fin)

    return pid
