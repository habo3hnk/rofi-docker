#!/usr/bin/env python

import sh
import sys


class DockerManager:
    def __init__(self):
        self.previous_select = "0"
        self.run_docker = sh.Command("docker")
        self.run_systemctl = sh.Command("systemctl")

    def rofi_menu(self, options: list, selected_option: str = "0") -> tuple:
        options_str = "\n".join(options)

        rofi_cmd = sh.Command("rofi")
        rofi_command = ["-dmenu", "-i"]
        if selected_option:
            rofi_command.extend(["-selected-row", selected_option])

        result = rofi_cmd(rofi_command, _in=options_str)
        current_choice = "0"
        if result:
            result = result.strip("\n")
            current_choice = options.index(result.strip("\n"))

        return (result, current_choice)

    def get_container_list(self) -> list[str]:
        try:
            containers = self.run_docker(
                "ps", "-a", "--format", "{{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
            )
            if containers:
                containers = containers.splitlines()
            else:
                containers = []
        except sh.ErrorReturnCode:
            containers = []

        containers.append("Stop Docker")
        return containers

    def check_docker_status(self):
        try:
            docker_status = self.run_systemctl("is-active", "docker")
            if docker_status:
                docker_status = docker_status.strip()
            if docker_status != "active":
                return False
            return True
        except sh.ErrorReturnCode:
            return False

    def handle_docker_inactive(self):
        action, _ = self.rofi_menu(["Start Docker", "Exit"])

        if action == "Start Docker":
            self.run_systemctl("start", "docker")
            self.run()
        else:
            sys.exit(1)

    def handle_container_action(self, container_id: str, current_choice: str):
        action, _ = self.rofi_menu(["Start", "Stop", "Restart", "Remove", "Back"])

        if action == "Start":
            self.run_docker("start", container_id)
        elif action == "Stop":
            self.run_docker("stop", container_id)
        elif action == "Restart":
            self.run_docker("restart", container_id)
        elif action == "Remove":
            self.run_docker("stop", container_id)
            self.run_docker("rm", container_id)
            self.previous_select = "0"
            return
        elif action == "Back":
            pass
        else:
            sys.exit(0)

        self.previous_select = current_choice

    def run(self):
        if not self.check_docker_status():
            self.handle_docker_inactive()
            return

        containers = self.get_container_list()

        selected = ""
        current_choice = ""
        if self.previous_select != "":
            selected, current_choice = self.rofi_menu(
                options=containers, selected_option=str(self.previous_select)
            )

        if not selected:
            sys.exit(1)

        if selected == "Stop Docker":
            self.run_systemctl("stop", "docker")
            sys.exit(0)

        container_id = selected.split()[0]
        self.handle_container_action(container_id, current_choice)
        self.run()


if __name__ == "__main__":
    manager = DockerManager()
    manager.run()
