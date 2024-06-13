import importlib

lambdas = [
    "app",
    "incorrect_noc",
    "incorrect_stop_type",
    "stop_not_found_in_naptan",
    "first_stop_is_set_down_only",
    "last_stop_is_pick_up_only",
    "first_stop_is_not_a_timing_point",
    "last_stop_is_not_a_timing_point",
]

from json import dumps

import argparse


def main():
    """
    Run lambda functions manually
    Command line example:
    python run_lambda.py --file_id=40 --check_id=1 --result_id=8
    """

    print("Here is the lamda list::::")
    for idx, name in enumerate(lambdas):
        print(f"{idx+1}: {name}")

    module_input = input("Choose the module from the above list ")
    parser = argparse.ArgumentParser(description="Run lambda functions manually")

    parser.add_argument("--file_id", help="A value for file_id", default=1)
    parser.add_argument("--check_id", help="A value for check_id", default=1)
    parser.add_argument("--result_id", help="A value for result_id", default=1)
    args = parser.parse_args()

    module_name = "app"
    if module_input.isdigit() and int(module_input) <= len(lambdas):
        module_name = lambdas[int(module_input) - 1]

    module_path = f"src.template.{module_name}"
    module = importlib.import_module(module_path)
    lambda_handler = module.lambda_handler

    print(
        f"Running the lambda: {module_path}::lambda_handler with file_id: {args.file_id}, check_id: {args.check_id}, result_id: {args.result_id}"
    )
    lambda_handler(
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
