#!/usr/bin/env python

import subprocess
import shlex
import sys


def run_command(command:str) -> subprocess.CompletedProcess:
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)
    return result


def rofi_menu(options:list, selected_option:int|bool=False) -> str and int:
    options_str = "\n".join(options)

    rofi_command = ["rofi", "-dmenu", "-i"]
    if selected_option:
        rofi_command.extend(["-selected-row", str(selected_option)])

    result = subprocess.run(
        rofi_command,
        input=options_str, 
        capture_output=True, 
        text=True
    ).stdout

    current_choise = 0

    if result:
        current_choise = options.index(result.strip('\n'))
    return result.strip(), current_choise


def get_container_list() -> list[str]:
    containers_result = run_command(
        "docker ps -a --format '{{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}'"
    )

    containers = containers_result.stdout.splitlines()
    containers.append("Stop Docker")

    if not containers:
        containers = ["Stop Docker"]

    return containers


def main(previous_select:bool|str=False) -> None:
    docker_status = run_command("systemctl is-active docker")
    if docker_status.returncode != 0:
        action, _ = rofi_menu(["Start Docker"])

        if action == "Start Docker":
            start_result = run_command("systemctl start docker")
            if start_result.returncode == 0:
                main()
            else:
                sys.exit(1)
        elif action == "Exit":
            print("Exiting...")
            sys.exit(1)
        else:
            print("Invalid action")
            sys.exit(1)


    containers = get_container_list()

    if previous_select != '':
        selected, current_choise = rofi_menu(
            options=containers,
            selected_option=previous_select
        )

    if not selected:
        print("No container selected")
        sys.exit(1)

    container_id = selected.split()[0]

    if selected == "Stop Docker":
        run_command("systemctl stop docker")
        sys.exit(0)

    action, _ = rofi_menu(
        [
            "Start",
            "Stop",
            "Restart",
            "Remove",
            "Back"
        ]
    )

    if action == "Start":
        run_command(f"docker start {container_id}")
        main(previous_select=current_choise)
    elif action == "Stop":
        run_command(f"docker stop {container_id}")
        main(previous_select=current_choise)
    elif action == "Restart":
        run_command(f"docker restart {container_id}")
        main(previous_select=current_choise)
    elif action == "Remove":
        run_command(f"docker stop {container_id}")
        run_command(f"docker rm {container_id}")
        main()
    elif action == "Back":
        main(previous_select=current_choise)
    else:
        print("Invalid action")
        sys.exit(0)

if __name__ == "__main__":
    main()
