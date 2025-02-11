# JSON Data Loading Guide

This guide provides instructions on how to load data from JSON files into the database. The JSON files contain data for words, groups, study activities, and other related entities.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7 or higher
- SQLite3
- SQLAlchemy

## Step-by-Step Instructions

### 1. Set Up the Virtual Environment

Create and activate a virtual environment for the project:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```
### 2.Run the Seed Script
```sh

python seed/seed_data.py
```

### 3.Verify Data

Verify that the data has been loaded correctly by checking the contents of the words.db file using `SQLite3`:

```sh
sqlite3 words.db
.tables

SELECT * FROM words;
SELECT * FROM study_activities;
```