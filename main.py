#!/usr/bin/env python3
# vi:ft=python3
from datetime import datetime, timezone
from subprocess import run, SubprocessError
from typing import Final

ALPHA_MAX: Final[int] = 7
BETA_MAX: Final[int] = 4
GAMMA_MAX: Final[int] = 6


# Press the green button in the gutter to run the script.
def rotate(maximum: int, unit: str, promote_from: str = None, ):
    try:
        run(['zfs', 'destroy', '-r', f'backup@{maximum}{unit}'])
    except SubprocessError:
        pass
    for i in range(maximum, 0, -1):
        try:
            run(['zfs', 'rename', '-r', f'backup@{i - 1}{unit}', f'backup@{i}{unit}'])
        except SubprocessError:
            pass
    if promote_from is not None:
        run(['zfs', 'rename', '-r', f'backup@{promote_from}', f'backup@0{unit}'])
    else:
        run(['zfs', 'snapshot', '-r', f'backup@0{unit}'])


if __name__ == '__main__':
    now = datetime.now(timezone.utc)
    cal = now.isocalendar()
    if cal.week % 4 == 1:  # every four weeks
        rotate(GAMMA_MAX, 'gamma', f'{BETA_MAX}beta')
    elif cal.weekday == 1:  # every seven days
        rotate(BETA_MAX, 'beta', f'{ALPHA_MAX}alpha')
    else:  # every day
        rotate(ALPHA_MAX, 'alpha')
