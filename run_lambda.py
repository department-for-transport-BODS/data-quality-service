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

def get_result_id_for_check_and_file(check_id, file_id):
    return db.session.scalar(
        select(TaskResults).where(
            (TaskResults.transmodel_txcfileattributes_id == file_id)
            & (TaskResults.checks_id == check_id)
        )
    )


def get_payload_for_mode(mode, data_flow, module, file_id, check_id, result_id):
    payload = None

    if mode == "SQS":
        payload = dict(Records=[
                    dict(body=dumps(dict(
                        file_id=file_id,
                        check_id=check_id,
                        result_id=result_id,
                    )))])
    elif mode == "SM":
        expected_pass = dict(
            last_stop_is_not_a_timing_point="first_stop_is_not_a_timing_point",
            no_timing_point_for_more_than_15_minutes="first_stop_is_not_a_timing_point",
            stop_not_found_in_naptan="first_stop_is_not_a_timing_point",
            missing_journey_code="first_stop_is_not_a_timing_point",
            last_stop_is_pick_up_only="first_stop_is_not_a_timing_point",
            first_stop_is_set_down_only="first_stop_is_not_a_timing_point"
        )
        if module in expected_pass.keys():
            payload = data_flow.get(expected_pass.get(module))
        else:
            payload = {
                "file_id": file_id
            }

    return payload

def run_lambda_func(file_id, check_id, mode, data_flow):

    print(f"FileId: {file_id}, CheckId: {check_id}")
    result_id = get_result_id_for_check_and_file(check_id, file_id)
    if not result_id:
        print(f"Result ID not found for file_id: {file_id}, check_id: {check_id}")
        return

    result_id = result_id.id
    print(f"Result ID: {result_id}")

    module_name = lambdas[check_id] if check_id in lambdas else "app"
    print(
        f"module_name: {module_name}, file_id: {file_id}, check_id: {check_id}, result_id: {result_id}"
    )

    module_path = f"src.template.{module_name}"
    if importlib.util.find_spec(module_path):
        module = importlib.import_module(module_path)
    else:
        module = importlib.import_module("src.template.app")
    lambda_handler = module.lambda_handler

    payload = get_payload_for_mode(mode, data_flow, module_name, file_id, check_id, result_id)
    print(
        f"Running the lambda: {module_path}::lambda_handler with file_id: {file_id}, check_id: {check_id}, result_id: {result_id}"
    )

    try:
         data_flow[module_name] =  lambda_handler(
            event=payload,
            context=Context(),
        )
    except Exception as e:
        print(f"Error running lambda: {e}, continuing")
    return data_flow


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
    parser.add_argument("--report_id", help="A value for report_id",default=None)
    parser.add_argument("--mode", help="Mode to run in",default="SQS", choices=["SQS", "SM"])

    args = parser.parse_args()
    file_id = args.file_id
    report_id = args.report_id
    mode = args.mode

    for key, val in lambdas.items():
        print(f"{key}: {val}")

    data_flow = dict() # Represents the passing of data from one lambda to the next
    first = 4
    if report_id: # Run all Data quality checks for selected report id 
        results = (db.session.query(TaskResults.transmodel_txcfileattributes_id)
        .distinct().where(TaskResults.dataquality_report_id == report_id)
        .all()
        )

        result_list = [result.transmodel_txcfileattributes_id for result in results]
        lambdas.pop("all")
        for file_id in result_list:
            data_flow = run_lambda_func(file_id, first, mode, data_flow)
            for check_id, _ in lambdas.items():
                if check_id == first: continue
                try:
                    data_flow = run_lambda_func(file_id, check_id, mode, data_flow)
                except Exception:
                    pass
    else:
        module_input = input("Choose the module from the above list ")
        # run for all lambdas
        if module_input == "all":
            lambdas.pop("all")
            data_flow = run_lambda_func(file_id, first, mode, data_flow)
            for check_id, _ in lambdas.items():
                if check_id == first: continue
                data_flow = run_lambda_func(file_id, check_id, mode, data_flow)
        else:
            module_input = int(module_input) if module_input.isdigit() else 0
            check_id = module_input
            data_flow = run_lambda_func(file_id, check_id, mode, data_flow)

if __name__ == "__main__":
    main()
