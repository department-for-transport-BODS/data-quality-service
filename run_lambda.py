import importlib
import importlib.util
import sys
from sqlalchemy import asc, select

sys.path.append("./src/boilerplate")

from common import BodsDB

db = BodsDB()
Checks = db.classes.dqs_checks
TaskResults = db.classes.dqs_taskresults


rs = db.session.query(Checks).order_by(asc(Checks.id)).all()
lambdas = {row.id: row.observation.lower().replace(" ", "_") for row in rs}
lambdas.update({"all": "all"})

rs = db.session.query(Checks).order_by(asc(Checks.id)).all()

from json import dumps
import argparse


class Context:
    def get_remaining_time_in_millis(self):
        return 135000

def run_lambda_func(file_id, check_id):

    print(f"FileId: {file_id}, CheckId: {check_id}")
    result_id = db.session.scalar(
        select(TaskResults).where(
            (TaskResults.transmodel_txcfileattributes_id == file_id)
            & (TaskResults.checks_id == check_id)
        )
    )
    result_id = result_id.id
    print(result_id)

    module_name = lambdas[check_id] if check_id in lambdas else "app"
    print(
        f"module_name: {module_name},  file_id: {file_id}, check_id: {check_id}, result_id: {result_id}"
    )

    module_path = f"src.template.{module_name}"
    if importlib.util.find_spec(module_path):
        module = importlib.import_module(module_path)
    else:
        module = importlib.import_module("src.template.app")
    lambda_handler = module.lambda_handler

    print(
        f"Running the lambda: {module_path}::lambda_handler with file_id: {file_id}, check_id: {check_id}, result_id: {result_id}"
    )
    lambda_handler(
        event={
            "Records": [
                {
                    "body": dumps(
                        obj={
                            "file_id": file_id,
                            "check_id": check_id,
                            "result_id": result_id,
                        }
                    )
                }
            ]
        },
        context=Context(),
    )


def main():
    """
    Run lambda functions manually
    Command line example:
    python run_lambda.py --file_id=40
    python run_lambda.py --report_id=50
    """

    print("Here is the lamda list::::")

    parser = argparse.ArgumentParser(description="Run lambda functions manually")
    parser.add_argument("--file_id", help="A value for file_id", default=1)
    parser.add_argument("--report_id", help="A value for file_id",default=None)
    args = parser.parse_args()
    file_id = args.file_id
    report_id = args.report_id

    for key, val in lambdas.items():
        print(f"{key}: {val}")

    if report_id: # Run all Data quality checks for selected report id 
        results = (db.session.query(TaskResults.transmodel_txcfileattributes_id)
        .distinct().where(TaskResults.dataquality_report_id == report_id)
        .all()
        )

        result_list = [result.transmodel_txcfileattributes_id for result in results]
        lambdas.pop("all")
        for file_id in result_list:
            for check_id, _ in lambdas.items():
                try:
                    run_lambda_func(file_id, check_id)
                except Exception:
                    pass
    else:
        module_input = input("Choose the module from the above list ")
        # run for all lambdas
        if module_input == "all":
            lambdas.pop("all")
            for check_id, _ in lambdas.items():
                run_lambda_func(file_id, check_id)
        else:
            module_input = int(module_input) if module_input.isdigit() else 0
            check_id = module_input
            run_lambda_func(file_id, check_id)


if __name__ == "__main__":
    main()
