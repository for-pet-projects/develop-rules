# ⚙️ Develop Rules & Engineering Standards

This repository provides unified development rules, workflows, and templates across several engineering domains — including Git, C/C++ (desktop & embedded), Python, and beyond.  
It aims to ensure consistency and clarity across teams and platforms.

---

## 📦 Quick Start

To create templates & wiki for your repo:

### ✅ Use a prebuilt archive

Download the latest `.run` file from the [Releases](https://github.com/<your-org>/<your-repo>/releases) page and execute it on any POSIX-compatible system:

```bash
chmod +x develop-rules-v*.run
./develop-rules-v*.run
```

### 🔧 Or build your own

If you want to build a customized version from source, follow the instructions in [`release/README.md`](release/README.md)

---

## 🗺️ Roadmap (2025)

| Area                      | Description                                               | Progress  |
| -                         | -                                                         | -         |
| ✅ Git & Workflow (Base)  | Branching, issues, naming, commit/PR policy               | **100%**  |
| 🟡 C/C++ Desktop          | Project layout, build system, logging, testing            | **20%**   |
| ⚪ C/C++ Embedded         | Bare-metal, RTOS, linker scripts, debugging               | **0%**    |
| ⚪ Python CLI             | Command-line tools, packaging, venv, typing, testing      | **0%**    |
| ⚪ PySide                 | Desktop GUI structure, integration with C++ core          | **0%**    |
| ⚪ Flutter / Dart         | Cross-platform GUI architecture, embedded integration     | **0%**    |
| ⚪ Go CLI                 | CLI structure, install/update flow, modular packaging     | **0%**    |
| ⚪ Bash / POSIX           | Scripting practices, modularity, cross-distro support     | **0%**    |

> Progress is approximate and updated manually

---

## 🤝 Contributing

Contributions are welcome!  
Please follow Git-related naming and branching rules described in [`git/`](./git), and submit well-scoped pull requests

---

## 📄 License

This project is licensed under the BSD 3-Clause License
You are free to use, modify, and redistribute the code and materials, provided that:.

- The original copyright and license are retained
- Binary redistributions include the same disclaimer
- The project name and author(s) are not used to promote derivative works without permission

See [LICENSE](./LICENSE) for full terms

