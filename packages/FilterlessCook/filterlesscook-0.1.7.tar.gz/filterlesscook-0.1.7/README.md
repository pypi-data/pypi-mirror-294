<p align="center">
    <h1 align="center">FILTERLESSCOOK</h1>
</p>
<p align="center">
    <em>Unique Data Recipes, No Filters Needed!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/last-commit/Bissbert/filterlesscook?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Bissbert/filterlesscook?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Bissbert/filterlesscook?style=default&color=0080ff" alt="repo-language-count">
<p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#overview)
- [ Getting Started](#getting-started)
    - [ Installation](#installation)
    - [ Usage](#usage)
        - [ Basic Usage](#basic-usage)
        - [ Options](#options)
        - [ Example](#example)
- [ Features](#features)
- [ Repository Structure](#repository-structure)
- [ Modules](#modules)
- [ License](#license)
</details>
<hr>

##  Overview

FilterlessCook is an innovative open-source Python package that streamlines recipe generation by eliminating the need for prefilters, offering a unique approach to data processing. This projects central module, `filterlesscook.py`, utilizes the ollama library and an AI assistant model for creating LaTeX-formatted recipes based on user prompts. With a focus on developer productivity, FilterlessCook allows developers to quickly create and save custom LaTeX documents using a single command, operating in an alpha stage under the MIT license. By using the FilterlessCook package, users can efficiently generate personalized food recipes without worrying about complicated setup or licensing issues.

---

##  Getting Started

**System Requirements:**

* **Python**: `version 3.6+`

### Installation

To install the FilterlessCook package, follow the instructions below:

```sh
pip install filterlesscook
```

If you want to use a specific version of the "dolphin-mixtral" model please preinstall, otherwise the tool will attempt to pull the newest version if none is already installed.

### Usage

To generate food recipes formatted as LaTeX using the `filterless-cook` command line tool, follow the instructions below:

#### Basic Usage
```
filterless-cook food
```
Replace `food` with the name of the food or product you want the recipe for.

#### Options

**-h, --help**: Show the help message and exit.
```
filterless-cook -h
```

**-p PROMPT, --prompt PROMPT**: Use a user-defined prompt for recipe generation.
```
filterless-cook food -p "Your custom prompt here"
```

**-f FILE, --file FILE**: Save the generated LaTeX document to the specified file path.
```
filterless-cook food -f /path/to/save/recipe.tex
```

**-m, --measurement MEASUREMENT**: Specify the type of measurement to be used in the recipes. Choose either 'metric' or 'imperial'. The default is 'metric'.
```
filterless-cook food -m imperial
```

**--debug**: Enable debug logging to see detailed log output.
```
filterless-cook food --debug
```

#### Example

To generate a chocolate cake recipe with a custom prompt and save it to `chocolate_cake.tex` with debug logging enabled:

```
filterless-cook "chocolate cake" -p "You are an expert baker with special experience in european cakes." -f chocolate_cake.tex --debug
```

---

##  Features

| Feature             | Description                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------|
| ⚙️ Architecture      | The project is a Python package with central functionality in `filterlesscook.py`. It utilizes the OLLAMA library for LaTeX document creation and interacts with AI assistants through chat interaction. |
| 🔩 Code Quality      | Well-organized code structure using Python, with adherence to the MIT license. Uses `setup.py` for distribution and easy installation via pip.                  |
| 📄 Documentation     | Provides essential documentation in both `README.md` and an informative LICENSE file. It explains usage, requirements, and development processes.              |
| 🔌 Integrations      | Utilizes OLLAMA library for LaTeX document creation, and incorporates user-defined prompts and chat interactions to generate recipes.                    |
| ⚡️ Performance        | Efficient LaTeX document generation, with potential room for improvement based on user's AI assistant model and requirements.                      |
| 🛡️ Security          | Utilizes local uncensored AI assistant models (dolphin-mixtral) to generate recipe text while prioritizing user privacy.                             |
| 📦 Dependencies      | Key external libraries include OLLAMA for LaTeX document creation, chat interaction interfaces and debug logging libraries.               |

---

##  Repository Structure

```sh
└── filterlesscook/
    ├── LISENCE
    ├── MANIFEST.in
    ├── filterlesscook
    │   ├── __init__.py
    │   └── filterlesscook.py
    └── setup.py
```

---

##  Modules

<details closed><summary>filterlesscook</summary>

| File                                                                                                         | Summary                                                                                                                                                                                                                                                                        |
| ---                                                                                                          | ---                                                                                                                                                                                                                                                                            |
| [filterlesscook.py](https://github.com/Bissbert/filterlesscook/blob/master/filterlesscook/filterlesscook.py) | LaTeX documents for recipes using ollama library and chat interaction, user-defined prompts, and saved to specified file paths. Utilizes debug logging and employs an uncensored AI assistant model (dolphin-mixtral) to generate recipe text, ensuring no kittens are harmed. |

</details>

---

##  License

This project is protected under the MIT License. For more details, refer to the [LICENSE](./LISENCE) file.

---

[**Return**](#overview)

---
