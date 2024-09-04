import logging
import argparse
import sys

from .metrics import GPUMetrics

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ROCm SMI Exporter command line flags."
    )

    parser.add_argument("--port", type=int, default=9001, help="Port number to use.")
    parser.add_argument(
        "--polling-interval-seconds",
        type=int,
        default=5,
        help="Polling interval in seconds.",
    )
    parser.add_argument(
        "--resolve-k8s-dev-alloc",
        type=bool,
        default=True,
        action=argparse.BooleanOptionalAction,
        help="If true, assume running inside k8s and resolve k8s info for GPU metrics",
    )
    parser.add_argument(
        "--ignore-non-k8s-metrics",
        type=bool,
        default=True,
        action=argparse.BooleanOptionalAction,
        help="If true, ignores metrics without k8s info",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()

    app_metrics = GPUMetrics(
        GPUMetrics.Config(
            port=args.port,
            polling_interval_seconds=args.polling_interval_seconds,
            resolve_k8s_dev_alloc=args.resolve_k8s_dev_alloc,
            ignore_non_k8s_metrics=args.ignore_non_k8s_metrics,
        )
    )
    app_metrics.run_read_metrcs_loop()


if __name__ == "__main__":
    main()
