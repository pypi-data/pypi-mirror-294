from pathlib import Path
from sys import argv, exit

from pkg_resources import get_distribution

from .internal.taskcontext import TaskContext
from .internal.tasks import tasks

dist = get_distribution("please_av1ppp")

pleasefile_names = [
    Path("Pleasefile.py"),
    Path("Pleasefile"),
]

init_command = ["-i", "-init"]
help_command = ["-h", "-help"]
version_command = ["-v", "-version"]

help_indent = "    "


def main():
    load_pleasefile_if_exists()

    args = argv[1:]

    if len(args) == 0 or args[0] in help_command:
        print_help()
        return

    if args[0] in init_command:
        init_pleasefile()
        return

    if args[0] in version_command:
        print_version()
        return

    if args[0] in tasks:
        task = tasks[args[0]]
        ctx = TaskContext(args[1:])
        task(ctx)
        return

    panic(f"Command or task '{args[0]}' not found. Try to use -h command.")


def init_pleasefile():
    filename = pleasefile_names[0]
    if filename.exists():
        panic("Pleasefile already created")

    with open(filename, mode="w") as file:
        file.write(
            """from please import TaskContext, task


@task()
def start(ctx: TaskContext):
    mode = ctx.string("mode") or "prod"
    print(f"*starting app in {mode} mode*")
"""
        )


def print_version():
    print("Please v" + dist.version)


def print_help():
    print("PLEASE - simple task runner.")
    print()

    print("COMMANDS:")
    print_command(init_command, "Create empty Pleasefile")
    print_command(help_command, "Show this message")
    print_command(version_command, "Show version")

    if len(tasks) > 0:
        print()
        print("TASKS:")
        for task_name, _ in tasks.items():
            print(f"{help_indent}{task_name}")


def load_pleasefile_if_exists():
    for filename in pleasefile_names:
        if not filename.exists():
            continue

        with open(filename, mode="r") as file:
            data = file.read()
            exec(data)
            return


def print_command(command: list, description: str):
    print(help_indent + ", ".join(command).ljust(26, " ") + description)


def panic(*values: object):
    print("ERROR:", *values)
    exit(1)


if __name__ == "__main__":
    main()
