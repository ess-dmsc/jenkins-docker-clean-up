# This Python file uses the following encoding: utf-8
import argparse
import sys
import datetime
import pytz
import docker


def print_stopping_criteria(max_running_time):
    msg = "Containers started more than {} hours ago will be stopped".format(
        max_running_time
    )
    print(msg)


def get_containers_to_stop(max_running_time):
    client = docker.from_env()

    containers_to_stop = []
    for container in client.containers.list():
        if container.attrs['State']['Status'] == 'running':
            started_at_datetime_utc = get_started_at_as_utc_datetime(container)
            delta = datetime.datetime.now(pytz.UTC) - started_at_datetime_utc
            if delta > max_running_time:
                containers_to_stop.append(container)

    return containers_to_stop


def get_started_at_as_utc_datetime(container):
    attrs = container.attrs
    started_at = truncate_str_at_seconds(attrs['State']['StartedAt'])
    # See comment in truncate_str_at_seconds for a sample datetime string
    started_at_datetime = datetime.datetime.strptime(
        started_at,
        "%Y-%m-%dT%H:%M:%S"
    )

    return pytz.UTC.localize(started_at_datetime)


def truncate_str_at_seconds(datetime_str):
    # A sample datetime string is 2018-05-16T13:20:19.76799975Z
    return datetime_str[:19]


def print_num_of_containers_to_stop(containers_to_stop):
    n = len(containers_to_stop)
    if n > 0:
        print("Will stop {} container".format(n) + ("s" if n > 1 else ""))
    else:
        print("No containers match the criteria for being stopped")


def stop_containers(containers):
    for container in containers_to_stop:
        print("Stopping container {}".format(container.id[:12]))
        container.stop()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("how_many_hours_is_too_long", type=int)
    args = arg_parser.parse_args()

    print_stopping_criteria(args.how_many_hours_is_too_long)

    # FIXME
    max_delta = datetime.timedelta(seconds=args.how_many_hours_is_too_long)
    containers_to_stop = get_containers_to_stop(max_delta)
    print_num_of_containers_to_stop(containers_to_stop)

    try:
        stop_containers(containers_to_stop)
    except Exception as e:
        print("Error when trying to stop containers:")
        print(e)
        sys.exit(1)

    sys.exit(0)
