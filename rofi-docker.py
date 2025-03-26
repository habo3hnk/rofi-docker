#!/usr/bin/env python

import sh
import sys


def rofi_menu(options: list, selected_option: str = "0") -> tuple:
    options_str = "\n".join(options)

    rofi_cmd = sh.Command("rofi")
    rofi_command = ["-dmenu", "-i"]
    if selected_option:
        rofi_command.extend(["-selected-row", selected_option])

    result = rofi_cmd(rofi_command, _in=options_str)
    current_choise = "0"
    if result:
        result = result.strip("\n")
        current_choise = options.index(result.strip("\n"))

    return (result, current_choise)


def get_container_list() -> list[str]:
    try:
        containers = sh.docker(
            "ps", "-a", "--format", "{{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
        )
        containers = containers.splitlines()
    except sh.ErrorReturnCode:
        containers = []

    containers.append("Stop Docker")
    return containers


def main(previous_select: str = "0") -> None:
    try:
        docker_status = sh.systemctl("is-active", "docker").strip()
        if docker_status != "active":
            action, _ = rofi_menu(["Start Docker"])

            if action == "Start Docker":
                sh.systemctl("start", "docker")
                main()
            elif action == "Exit":
                sys.exit(1)
            else:
                sys.exit(1)
            return
    except sh.ErrorReturnCode:
        action, _ = rofi_menu(["Start Docker"])

        if action == "Start Docker":
            sh.systemctl("start", "docker")
            main()
        elif action == "Exit":
            sys.exit(1)
        else:
            sys.exit(1)
        return

    containers = get_container_list()

    selected = ""
    current_choice = ""
    if previous_select != "":
        selected, current_choice = rofi_menu(
            options=containers, selected_option=str(previous_select)
        )

    if not selected:
        sys.exit(1)

    container_id = selected.split()[0]

    if selected == "Stop Docker":
        sh.systemctl("stop", "docker")
        sys.exit(0)

    action, _ = rofi_menu(["Start", "Stop", "Restart", "Remove", "Back"])

    if action == "Start":
        sh.docker("start", container_id)
        main(previous_select=current_choice)
    elif action == "Stop":
        sh.docker("stop", container_id)
        main(previous_select=current_choice)
    elif action == "Restart":
        sh.docker("restart", container_id)
        main(previous_select=current_choice)
    elif action == "Remove":
        sh.docker("stop", container_id)
        sh.docker("rm", container_id)
        main()
    elif action == "Back":
        main(previous_select=current_choice)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
