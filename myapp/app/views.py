import pandas as pd
import json
from django.shortcuts import render
from .models import Product

def upload_csv(request):
    data = None
    total_sales = None
    total_quantity = None
    average_sales_per_day = None

    if request.method == 'POST' and request.FILES['csv']:
        csv_file = request.FILES['csv']
        try:
            data = pd.read_csv(csv_file)

            data.dropna(inplace=True)
            data['amount'] = pd.to_numeric(data['amount'], errors='coerce')
            data['date'] = pd.to_datetime(data['date'], errors='coerce')
            data.dropna(inplace=True)

            total_sales = data.groupby('product')['amount'].sum().reset_index()
            total_quantity = data.groupby('product')['quantity'].sum().reset_index()

            for index, row in total_sales.iterrows():
                product_name = row['product']
                total_amount = row['amount']
                quantity = total_quantity.loc[total_quantity['product'] == product_name, 'quantity'].values[0]

                Product.objects.update_or_create(
                    product=product_name,
                    defaults={
                        'total_amount': total_amount,
                        'quantity': quantity
                    }
                )

            # Calculate average sales per day
            daily_sales = data.groupby('date')['amount'].sum()
            average_sales_per_day = daily_sales.mean()

        except Exception as e:
            print(f"Error processing the CSV file: {e}")
            data = pd.DataFrame()
            total_sales = pd.DataFrame()
            total_quantity = pd.DataFrame()
            average_sales_per_day = 0

    return render(request, 'upload.html', {
        'data': data,
        'total_sales': total_sales,
        'total_quantity': total_quantity,
        'average_sales_per_day': average_sales_per_day
    })



def sales_chart(request):
    total_sales = Product.objects.all()
    chart_labels = [product.product for product in total_sales]
    chart_data = [float(product.total_amount) for product in total_sales]

    line_chart_labels = []
    line_chart_data = []
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    print(f"Start Date: {start_date}, End Date: {end_date}")

    if start_date and end_date:
        try:
            daily_sales = pd.read_csv('/home/bhavya/Desktop/Bhavya/sales_data .csv')  # Corrected path
            daily_sales['date'] = pd.to_datetime(daily_sales['date'], errors='coerce')

            mask = (daily_sales['date'] >= pd.to_datetime(start_date)) & (daily_sales['date'] <= pd.to_datetime(end_date))
            filtered_sales = daily_sales[mask]

            print(f"Filtered Sales Data: {filtered_sales}")

            daily_average_sales = filtered_sales.groupby('date')['amount'].mean().reset_index()
            line_chart_labels = daily_average_sales['date'].dt.strftime('%Y-%m-%d').tolist()
            line_chart_data = daily_average_sales['amount'].tolist()

            print(f"Line Chart Labels: {line_chart_labels}")
            print(f"Line Chart Data: {line_chart_data}")

        except Exception as e:
            print(f"Error processing daily sales data: {e}")

    return render(request, 'sales_chart.html', {
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'line_chart_labels': json.dumps(line_chart_labels),
        'line_chart_data': json.dumps(line_chart_data),
    })

