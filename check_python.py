import sys

NEEDED_MAJOR = 3
NEEDED_MINOR = 12
if not (
    sys.version_info.major == NEEDED_MAJOR and sys.version_info.minor >= NEEDED_MINOR
):
    print(
        f"Invalid python version ({sys.version_info.major}.{sys.version_info.minor}) please use at least {NEEDED_MAJOR}.{NEEDED_MINOR}"
    )
    exit(1)
