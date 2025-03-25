# rofi-docker

This Python script provides a convenient way to manage Docker containers using a graphical menu created with **Rofi**. It allows you to start, stop, restart, and remove Docker containers, as well as manage the Docker service itself through an interactive menu.

### Key Features:
- **Docker Service Management**:
  - Start or stop the Docker service if it is not active.
- **Container Management**:
  - Display a list of all Docker containers (both running and stopped).
  - Start, stop, restart, or remove selected containers.

### Requirements:
- **Python 3.x**
- **Rofi** (for the graphical menu)
- **Docker** (installed and configured)
- **sh** library (pip install sh)

### Usage:
1. Make the script executable:
   ```bash
   chmod +x docker_rofi.py
   ```
2. Run the script:
   ```bash
   ./docker_rofi.py
   ```
3. Use the Rofi menu to:
   - Start or stop the Docker service.
   - Select a container and perform actions (start, stop, restart, remove).

### Example Workflow:
1. If Docker is not running, the script will prompt you to start it.
2. Once Docker is running, a list of all containers will be displayed.
3. Select a container and an action (e.g., start, stop, restart, remove).
4. After performing the action, you can return to the container list or exit.

### Notes:
**Your user must be a member of the `docker` group.**

Below is an example of how to add a user to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

After running this command, log out and log back in for the changes to take effect. You can then verify that Docker works without `sudo` by running:

```bash
docker run hello-world
```
