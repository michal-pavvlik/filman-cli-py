# filman - CLI File Manager

Lightweight file manager, made with Python, created specifically for Linux terminal environment.

## 🚀 Features

`filman` provides a streamlined interface for core system operations:
* **Add:** Create new files instantly
* **Delete:** Remove files from the system
* **Edit:** Modify file contents directly in CLI
* **Move:** Move a file between directories
* **Undo:** Made a mistake? No problem, just undo it.

## 🛠️  Requirements

* Linux OS
* Python 3.x

## 💻 Usage

1. Add script to executables

```bash
chmod +x filman.py
```

2. To launch the file manager simply write path the script, eg. In filman directory:

```bash
./filman.py --help
```

3. [Recommended] Script may be used just as any terminal tool. Just add its path to executables.
* Create local bin directory (if it doesn't already exists)
```bash
mkdir ~/.local/bin
```
* Create a symbolic link. Go to filman catalog and run:
```bash
ln -s "$(pwd)/filman.py" ~/.local/bin/filman
```
* Ensure bin folder is in PATH. In most distros not needed to do (done automatically)
```bash
export PATH="$HOME/.local/bin:$PATH"
```
* Now just write
```bash
filman --help
```