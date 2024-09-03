# Pre-requisites
- Python 3.11 or higher.
- Ubuntu 22.04 or higher.
- Install the dependencies Ubuntu packages:
  ```bash
  sudo apt update &&
  sudo apt install -y translate-shell xclip libxcb-cursor-dev --upgrade
  ```
  
- Install required Python packages:
  ```bash
  pip install -r requirements.txt --upgrade
  ```

- Install `kleantrans`:
  ```bash
  # Ubuntu 23.04 or higher, Python 3.12 or higher
  pip3 install kleantrans --upgrade --break-system-packages
  
  # Remaining cases
  pip3 install kleantrans --upgrade
  ```