import json
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime
import os

class BpiGraphGenerator:
    def __init__(self, json_path, output_dir):
        self.json_path = json_path
        self.output_dir = output_dir
        self.line_graph_path = os.path.join(output_dir, "bpi_line_graph.png")
        self.candle_graph_path = os.path.join(output_dir, "bpi_candlestick.png")

    def load_data(self) -> pd.DataFrame:
        with open(self.json_path, 'r') as f:
            data = json.load(f)
        
        if not data:
            return pd.DataFrame()

        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df['price'] = df['price'].astype(float)
        return df

    def generate_line_chart(self, df: pd.DataFrame):
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df['price'], marker='o', linestyle='-', color='#00ffcc')
        plt.title("Bitcoin Price Index (Line Chart)", color='white')
        plt.xlabel("Time", color='white')
        plt.ylabel("Price (USD)", color='white')
        plt.grid(True, color='gray', linestyle='--', alpha=0.5)
        
        # Dark mode styling
        plt.gca().set_facecolor('#1e1e1e')
        plt.gcf().patch.set_facecolor('#1e1e1e')
        plt.tick_params(colors='white')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.line_graph_path, facecolor='#1e1e1e')
        plt.close()

    def generate_candlestick_chart(self, df: pd.DataFrame):
        # Resample data to 5-minute intervals for the candlestick (OHLC)
        ohlc = df['price'].resample('5min').ohlc()
        ohlc.dropna(inplace=True)

        if ohlc.empty:
            return # Not enough data for candlestick

        # Dark mode style for mplfinance
        mc = mpf.make_marketcolors(up='g', down='r', edge='inherit', wick='inherit', volume='in')
        s  = mpf.make_mpf_style(marketcolors=mc, facecolor='#1e1e1e', edgecolor='white', figcolor='#1e1e1e', gridcolor='gray')

        mpf.plot(ohlc, type='candle', style=s, title="Bitcoin Price Index (Candlestick - 5m)", 
                 ylabel='Price (USD)', savefig=self.candle_graph_path)

    def generate_all_graphs(self):
        df = self.load_data()
        if df.empty:
            return None, None
            
        self.generate_line_chart(df)
        self.generate_candlestick_chart(df)
        
        return self.line_graph_path, self.candle_graph_path