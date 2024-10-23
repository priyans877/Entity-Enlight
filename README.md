
# 🌟 Entity Enlight 🌟

[![GitHub repo](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/priyans877/Entity-Enlight)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Introduction
**Entity Enlight** is a text extraction and entity recognition tool that processes text from various sources including website URLs, PDFs, and user inputs. The application extracts the text, generates a summary, and identifies related entities, classifying them into categories such as people, organizations, locations, and more. This is achieved using an interactive interface built with Streamlit.

## Features
- **Text Extraction**: Supports extracting text from website URLs, PDF files, and user-provided input.
- **Entity Recognition**: Automatically identifies and categorizes entities such as names, places, dates, and organizations.
- **Summary Generation**: Provides a concise summary of the extracted text.
- **Streamlit Interface**: Intuitive interface for uploading files, entering URLs, or typing text directly.

## Installation
To set up the project locally, follow the steps below:

### Prerequisites
- Python 3.7 or higher
- [Git](https://git-scm.com/)
- Required Python libraries: see `requirements.txt`

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/priyans877/Entity-Enlight.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Entity-Enlight
   ```
3. Create a virtual environment:
   ```bash
   python -m venv env
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```
5. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
After setting up the environment, start the Streamlit app using:

```bash
streamlit run app.py
```

### Input
- You can either:
  - Upload a PDF document.
  - Provide a website URL.
  - Enter text manually.

### Output
- The application will display:
  - A summary of the extracted text.
  - Identified entities categorized by type (e.g., people, organizations, locations).

## Technologies Used
- **Python**: Programming language used for core development.
- **spaCy / NLTK**: For natural language processing and entity recognition.
- **Streamlit**: Framework for building the interactive user interface.
- **PDFMiner**: For extracting text from PDFs.
- **BeautifulSoup**: For web scraping to extract text from URLs.

## Contributing
Contributions are encouraged! Here's how you can contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add feature XYZ'`).
4. Push the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For more information, visit the repository: [Entity Enlight](https://github.com/priyans877/Entity-Enlight).
