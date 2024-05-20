#!/bin/bash

queues=(
  "incorrect_licence_number_queue"
  "same_stop_found_multiple_times_queue"
  "stops_not_found_in_queue"
  "missing_stops_queue"
  "missing_bus_working_number_queue"
  "duplicate_journey_code_queue"
  "missing_journey_code_queue"
  "incorrect_stop_type_queue"
  "last_stop_is_not_a_timing_point_queue"
  "first_step_is_not_a_timing_point_queue"
  "last_stop_is_pickup_only_queue"
  "first_stop_is_set_down_only_queue"
  "incorrect_noc_queue"
)

for queue in "${queues[@]}"; do
  awslocal sqs create-queue --queue-name "$queue"
done
