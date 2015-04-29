# Copyright 2015 Red Hat Inc., Durham, North Carolina.
# All Rights Reserved.
#
# scap-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.
#
# scap-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with scap-client.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Martin Preisler <mpreisle@redhat.com>

from scap_client import dbus_daemon

import dbus
import gobject
import argparse
import sys


def get_dbus_interface():
    gobject.threads_init()

    # bus = dbus.SystemBus()
    # for easier testing
    bus = dbus.SessionBus()
    if bus is None:
        return None

    obj = bus.get_object(
        dbus_daemon.BUS_NAME,
        dbus_daemon.OBJECT_PATH
    )

    if obj is None:
        return None

    return dbus.Interface(obj, dbus_daemon.DBUS_INTERFACE)


def cli_task(dbus_iface, args):
    if args.task_id is None:
        task_ids = dbus_iface.ListTaskIDs()

        for task_id in task_ids:
            title = dbus_iface.GetTaskTitle(task_id)
            print("%i\t\t%s\t\t..." % (task_id, title))

    else:
        title = dbus_iface.GetTaskTitle(args.task_id)

        print("ID:\t%i" % (args.task_id))
        print("Title:\t%s" % (title))

        # TODO


def cli_status(dbus_iface, args):
    pass


def cli_results(dbus_iface, args):
    pass


def main():
    dbus_iface = get_dbus_interface()

    if dbus_iface is None:
        print("Error: Failed to connect to SCAP Client dbus interface.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="SCAP Client command line interface."
    )
    subparsers = parser.add_subparsers()

    task_parser = subparsers.add_parser(
        "task",
        help="Show info about tasks that have already been defined."
    )
    task_parser.set_defaults(action="task")
    task_parser.add_argument(
        "task_id", metavar="TASK_ID", type=int, nargs="?",
        help="ID of the task to display, if none is provided a summary of all "
        "tasks is displayed"
    )

    status_parser = subparsers.add_parser(
        "status",
        help="Displays status, tasks that are planned and tasks that are being "
        "evaluated."
    )
    status_parser.set_defaults(action="status")

    result_parser = subparsers.add_parser(
        "result",
        help="Displays info about past results"
    )
    result_parser.add_argument(
        "task_id", metavar="TASK_ID", type=int
    )
    result_parser.add_argument(
        "result_id", metavar="RESULT_ID", type=int, nargs="?",
        help="ID of the result we want to display, if none is provided "
        "a summary of all results of given task is displayed."
    )
    result_parser.add_argument(
        "format", metavar="FORMAT", type=str,
        choices=["html", "arf"], default="arf", nargs="?"
    )
    result_parser.set_defaults(action="result")

    args = parser.parse_args()

    if args.action == "task":
        cli_task(dbus_iface, args)
    elif args.action == "status":
        cli_status(dbus_iface, args)
    elif args.action == "result":
        cli_results(dbus_iface, args)
    else:
        raise RuntimeError("Unknown action '%s'." % (args.action))


if __name__ == "__main__":
    main()