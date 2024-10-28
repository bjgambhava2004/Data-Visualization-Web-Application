# Sales Analysis App

A Django application to upload sales data in CSV format, visualize total sales amounts per product, and analyze daily average sales over a specified period.

## Features

- Upload CSV files containing sales data.
- View total sales amount and quantity per product.
- Generate bar and line charts for sales visualization.
- Select a date range to analyze daily average sales.

## Requirements

- Python 3.x
- Django 4.x
- pandas
- Chart.js (included in the templates)

## Installation & How to run

1. **Clone the repository:**

   ```bash
   git clone https://your-repository-url.git
   cd sales_analysis_app

2. **Install the required packages:**

   ```bash
   pip install django pandas

3. **Create the database:**

   ```bash
   python manage.py migrate

4. **Run the development server:**

   ```bash
   python manage.py runserver

5. **Open your web browser and go to:**

   ```bash
   http://127.0.0.1:8000/


