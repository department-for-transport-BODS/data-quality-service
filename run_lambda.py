from src.template.app import lambda_handler

from src.template.stop_not_found_in_naptan import (
    lambda_handler as stop_not_found_in_naptan_lambda_handler,
)
from src.template.incorrect_stop_type import (
    lambda_handler as incorrect_stop_type_lambda_handler,
)
from src.template.last_stop_is_pick_up_only import (
    lambda_handler as last_stop_is_pick_up_only_lambda_handler,
)
from src.template.last_stop_is_timing_point import (
    lambda_handler as last_stop_is_timing_point_lambda_handler,
)
from json import dumps

import argparse


def main():
    """
    Run lambda functions manually
    Command line example:
    python run_lambda.py --function_name=stop_not_found_in_naptan_lambda_handler --file_id=40 --check_id=1 --result_id=8
    """
    parser = argparse.ArgumentParser(description="Run lambda functions manually")
    parser.add_argument(
        "--function_name", help="Add function name to run", default="lambda_handler"
    )
    parser.add_argument("--file_id", help="A value for file_id", default=1)
    parser.add_argument("--check_id", help="A value for check_id", default=1)
    parser.add_argument("--result_id", help="A value for result_id", default=1)
    args = parser.parse_args()
    functions_to_run = {
        "lambda_handler": lambda_handler,
        "incorrect_stop_type_lambda_handler": incorrect_stop_type_lambda_handler,
        "stop_not_found_in_naptan_lambda_handler": stop_not_found_in_naptan_lambda_handler,
        "last_stop_is_pick_up_only_lambda_handler": last_stop_is_pick_up_only_lambda_handler,
        "last_stop_is_timing_point_lambda_handler": last_stop_is_timing_point_lambda_handler,
    }

    functions_to_run[args.function_name](
        event={
            "Records": [
                {
                    "body": dumps(
                        obj={
                            "file_id": args.file_id,
                            "check_id": args.check_id,
                            "result_id": args.result_id,
                        }
                    )
                }
            ]
        },
        context=None,
    )


if __name__ == "__main__":
    main()
