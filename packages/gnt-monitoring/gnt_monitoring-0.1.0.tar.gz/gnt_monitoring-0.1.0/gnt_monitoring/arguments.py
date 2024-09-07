import argparse


def base_args() -> argparse.ArgumentParser:
    args = argparse.ArgumentParser()
    general = args.add_argument_group(title="General options")
    sentry = args.add_argument_group(title="Sentry")
    general.add_argument(
        "--log-level",
        help=("Log level, default: %(default)s"),
        default="warning",
        choices=["debug", "info", "warning", "critical", "error"],
        type=str
    )
    general.add_argument(
        "--warning",
        help="Warning value, default: %(default)f",
        default=75,
        type=float
    )
    general.add_argument(
        "--critical",
        help="Critical value, default: %(default)f",
        default=90,
        type=float
    )
    sentry.add_argument(
        "--sentry-dsn",
        help="Sentry dsn for remote error logging",
        type=str
    )
    sentry.add_argument(
        "--sentry-env",
        help="Envronment name for sentry, defaul: %(default)s",
        default="dev",
        type=str
    )
    return args


def arguments() -> argparse.Namespace:
    args = base_args()
    return args.parse_args()
