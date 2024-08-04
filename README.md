# NEET UG-2024 AP Results Viewer

This Streamlit application allows users to view and filter NEET UG-2024 results for candidates from Andhra Pradesh. The app fetches data from a SQLite database and provides an intuitive interface for filtering based on score, gender, category, and NEET roll number.

## Features

- **Data Ingestion**: Load NEET UG-2024 results from a CSV file into a SQLite database.
- **Interactive Filtering**: Filter results based on score, gender, category, and NEET roll number.
- **Streamlit Interface**: User-friendly interface with custom styling and light mode enabled.
- **Author Section**: Includes author information and description of the data source.

## How to Run

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/neet-ug-2024-ap-results-viewer.git
    cd neet-ug-2024-ap-results-viewer
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Create the SQLite database and load data**:
    ```sh
    python create_db.py
    ```

4. **Run the Streamlit app**:
    ```sh
    streamlit run app.py
    ```

## Project Structure

```
neet-ug-2024-ap-results-viewer/
├── .streamlit/
│   └── config.toml        # Streamlit configuration for light mode
├── data/
│   └── neet_results.csv   # CSV file containing NEET UG-2024 results
├── create_db.py           # Script to create SQLite database and load data
├── app.py                 # Main Streamlit application script
├── requirements.txt       # Python dependencies
└── README.md              # Project description and setup instructions
```

