# Project Title
**CTA L Analysis App**

This project is designed to analyze and generate general statistics from the CTA L system, providing insights into the number of stations, stops, and ride entries. The application is built to facilitate quick analysis and visualization of transit data, making it a useful tool for anyone interested in urban transit analytics.

## Project Description
The **CTA L Analysis App** is a Python-based application that interacts with a SQLite database containing data related to the Chicago Transit Authority's L system. The app retrieves various statistics from the database, including the number of stations, stops, and ride entries, and visualizes the data using Matplotlib.

### Key Features:
- **Database Interaction:** The app connects to a SQLite database to fetch and analyze data.
- **Data Visualization:** Using Matplotlib, the app generates visual representations of the data, making it easier to understand trends and patterns.
- **Extensible:** The code is modular, allowing for easy extensions or modifications to include additional data sources or analyses.

### Technologies Used:
- **Python:** The primary programming language used for developing the app.
- **SQLite:** A lightweight database management system used for storing and querying the CTA L system data.
- **Matplotlib:** A plotting library used for creating static, animated, and interactive visualizations in Python.

### Challenges Faced:
- **Data Integrity:** Ensuring that the data retrieved from the database is accurate and up-to-date.
- **Performance Optimization:** Efficiently querying large datasets to provide quick insights.
- **Scalability:** Designing the app in a way that allows easy integration of new features or data sources.

## Table of Contents
- [Project Title](#project-title)
- [Project Description](#project-description)
- [Table of Contents](#table-of-contents)
- [How to Install and Run the Project](#how-to-install-and-run-the-project)
- [How to Use the Project](#how-to-use-the-project)

## How to Install and Run the Project

### Prerequisites
- **Python 3.x**: Make sure you have Python 3.x installed on your machine.
- **SQLite**: The app uses a SQLite database, so ensure that SQLite is installed and properly configured.

### Installation Steps
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/cta-l-analysis-app.git
    cd cta-l-analysis-app


2. **Set up a Virtual Environment (Optional but recommended):**
    ```bash
     git clone https://github.com/yourusername/cta-l-analysis-app.git
     cd cta-l-analysis-app

3. **Install the Required Packages:**

    ```bash
    Copy code
    pip install -r requirements.txt

4. **Prepare the Database:**

Download and place the CTA2_L_daily_ridership.db SQLite database file into the project directory (the same directory as main.py).


5. **Run the Application:**

    ```bash
    python main.py

## How to Use the Project

1. **Execute Basic Statistics:**
   - Upon running the application, the app will connect to the SQLite database and execute various SQL queries to retrieve and output basic statistics related to the CTA L system.

2. **Visualize Data:**
   - The application will also generate visualizations using Matplotlib, which can be used to understand data trends over time.

3. **Extend Functionality:**
   - The modular structure of the code allows you to add more functions to analyze different aspects of the dataset or to visualize data in new ways.

### Example:
```python
# Example of how to add a new statistic to be calculated:
def new_stat_function(dbConn):
    dbCursor = dbConn.cursor()
    # Your SQL query and data processing logic here
    # e.g., dbCursor.execute('SELECT * FROM new_table')
    dbCursor.close()
