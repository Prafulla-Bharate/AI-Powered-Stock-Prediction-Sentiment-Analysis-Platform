from django.core.management.base import BaseCommand,CommandError
from apps.models import Stock, StockPrice
from apps.utils import fetch_stock_data
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Fetch historical stock data for all stocks in the database'

    def handle(self, *args, **options):
        stocks = Stock.objects.all()
        if not stocks.exists():
            self.stdout.write(self.style.WARNING('No stocks found in the database.'))
            return

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Fetch last year by default

        for stock in stocks:
            self.stdout.write(f"Fetching data for {stock.ticker}...")
            history_df = fetch_stock_data(stock.ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

            if history_df.empty:
                self.stdout.write(self.style.WARNING(f"No data found for {stock.ticker}."))
                continue

            # Save to DB
            for _, row in history_df.iterrows():
                StockPrice.objects.update_or_create(
                    stock=stock,
                    date=row['date'],
                    defaults={
                        'open_price': row['open'],
                        'high_price': row['high'],
                        'low_price': row['low'],
                        'close_price': row['close'],
                        'volume': row['volume']
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Data for {stock.ticker} updated successfully.")) 