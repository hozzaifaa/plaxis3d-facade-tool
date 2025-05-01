# PLAXIS 3D Simplified Building Facade Tool

This Python script automates the creation of a simplified building facade within PLAXIS 3D.  
It generates structural elements like walls, windows, doors, lintels, and footings using fixed geometric parameters and a graphical input for position and orientation.

---

## 🚀 Features

- Creates facade geometry with windows, doors, and lintels
- Automatically includes footings and wall thickness
- Simple GUI input for x/y offset and rotation angle
- Integrates with PLAXIS 3D through `plxscripting.easy`

---

## 🔧 Requirements

- **PLAXIS 3D** (with Python scripting enabled)
- Python libraries:
  - `plxscripting`
  - `easygui`

---

## 📌 Installation and Usage

### ➤ Install the Script as a PLAXIS Tool:

1. Download the Python file from this repository.
2. Copy the script into this folder:

<PLAXIS 3D installation folder>\pytools\input


Typical installation paths include:
- `C:\Program Files\Seequent\`
- `C:\Program Files\Bentley\Geotechnical\`
- `C:\Program Files\Plaxis\Plaxis 3D\` (older versions)

3. Restart **PLAXIS 3D**.
4. Open a project.
5. Switch to **Staged Construction** mode.
6. Go to:  
   **Expert > Python > Run script > Tools**, and select the script name.
7. Enter the requested offsets and rotation when prompted.  
   The tool will generate the facade and output confirmation.

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE.txt).  
You are free to use, modify, and distribute this tool — including for commercial purposes — as long as you retain the original license.

---

## 🛠 Author

**Unina Automation**  
This tool was developed as part of a research and automation effort in geotechnical modeling with PLAXIS 3D.

