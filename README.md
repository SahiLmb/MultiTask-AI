# Multitask Pro: Unified AI-Powered Data Retrieval

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Overview

Multitask Pro is a powerful AI-driven application designed to transform natural language inputs into SQL queries. It enables users to effortlessly interact with databases containing PropertyRecords, HealthcareRecords, and FinanceRecords. The app makes data retrieval intuitive and user-friendly, providing conversational responses.

## Features

- **Natural Language Processing**: Converts user inputs into SQL queries.
- **Database Interaction**: Executes SQL queries on PropertyRecords, HealthcareRecords, and FinanceRecords databases.
- **Conversational Responses**: Formats retrieved data into natural language responses.
- **Multi-Domain Support**: Handles property, healthcare, and finance records.

## How It Works

1. **User Input**: The user types a plain language query, such as "Show me all residential properties in Mumbai."
2. **NLP Conversion**: Advanced AI models convert the user's input into a SQL query.
3. **Database Execution**: The SQL query is executed on the relevant database.
4. **Data Retrieval**: Relevant data is fetched from the database.
5. **Natural Language Response**: The data is formatted into a conversational response and displayed to the user.

## Setup and Installation

### Prerequisites

- Python 3.7 or higher
- SQLite3
- Streamlit
- Google Generative AI

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/SahiLmb/gemini-prog.git
    cd multitask-pro
    ```

2. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a `.env` file in the root directory and add your Google API key:

    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

4. **Initialize the SQLite database:**

    ```sh
    python initialize_database.py
    ```

### Files and Directories

- `initialize_database.py`: Script to create and populate the SQLite database.
- `app.py`: Main Streamlit application file.
- `requirements.txt`: List of required Python packages.
- `.env`: Environment variables file.

## Usage

1. **Run the Streamlit app:**

    ```sh
    streamlit run app.py
    ```

2. **Access the application:**

    Open your web browser and go to `http://localhost:8501`.

3. **Navigate through the app:**

    Use the sidebar to switch between querying PropertyRecords, HealthcareRecords, and FinanceRecords.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to [Google Generative AI](https://ai.google/) for their powerful NLP tools.
- Special thanks to the contributors and open-source community.

---
