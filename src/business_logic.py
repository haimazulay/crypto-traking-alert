import time
import os
from src.api_client import CoinbaseApiClient
from src.storage import JsonStorage
from src.visualizer import BpiGraphGenerator
from src.notifier import EmailNotifier
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
from rich.terminal_theme import MONOKAI

# Initialize Rich Console with recording enabled
console = Console(record=True)

class TrackerBusinessLogic:
    def __init__(self, config):
        self.config = config
        self.api_client = CoinbaseApiClient(config.API_URL)
        self.storage = JsonStorage(config.JSON_FILE_PATH)
        self.visualizer = BpiGraphGenerator(config.JSON_FILE_PATH, config.OUTPUT_DIR)
        
        # Note: If no password is provided in .env, notifier will be skipped gracefully
        self.notifier = None
        if config.SENDER_PASSWORD:
            self.notifier = EmailNotifier(config.SENDER_EMAIL, config.SENDER_PASSWORD, config.RECEIVER_EMAIL)

    def generate_html_dashboard(self, max_price: float, line_path: str, candle_path: str):
        console.print("[bold cyan]Generating HTML Dashboard...[/bold cyan]")
        
        # Export the Rich terminal output to HTML
        terminal_html = console.export_html(theme=MONOKAI, clear=False)
        
        # Create a beautiful dark-mode dashboard
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>BPI Live Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; padding: 20px; }}
                h1 {{ color: #00ffcc; text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                .stats-card {{ background-color: #1e1e1e; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px; border: 1px solid #333; }}
                .stats-card h2 {{ color: #ff9900; margin: 0; font-size: 2.5em; }}
                .graphs-container {{ display: flex; flex-wrap: wrap; justify-content: space-around; gap: 20px; margin-bottom: 40px; }}
                .graph-box {{ background-color: #1e1e1e; padding: 10px; border-radius: 8px; border: 1px solid #333; flex: 1; min-width: 400px; text-align: center; }}
                .graph-box img {{ max-width: 100%; border-radius: 4px; }}
                .terminal-box {{ background-color: #000000; padding: 20px; border-radius: 8px; border: 1px solid #333; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <h1>🚀 BPI Automation Execution Report</h1>
            
            <div class="stats-card">
                <p>Maximum Price Recorded</p>
                <h2>${max_price:,.2f}</h2>
            </div>

            <div class="graphs-container">
                <div class="graph-box">
                    <h3>Line Chart</h3>
                    <img src="{os.path.basename(line_path)}" alt="Line Chart">
                </div>
                <div class="graph-box">
                    <h3>Candlestick Chart (5m)</h3>
                    <img src="{os.path.basename(candle_path)}" alt="Candlestick Chart">
                </div>
            </div>

            <h2>Execution Logs</h2>
            <div class="terminal-box">
                {terminal_html}
            </div>
        </body>
        </html>
        """
        
        dashboard_path = os.path.join(self.config.OUTPUT_DIR, "index.html")
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        console.print(f"[bold green]Dashboard created successfully at {dashboard_path}[/bold green]")

    def run(self):
        console.print(Panel.fit("[bold green]Starting BPI Tracker System[/bold green]", border_style="green"))
        max_price = 0
        iterations = self.config.TOTAL_MINUTES
        
        for i in track(range(iterations), description="[cyan]Monitoring BTC Price..."):
            price = self.api_client.get_current_bpi()
            
            if price:
                console.print(f"[green]✔ Iteration {i+1}/{iterations}: BTC Price is ${price:,.2f}[/green]")
                self.storage.save_record(price)
                if price > max_price:
                    max_price = price
            else:
                console.print(f"[red]✖ Failed to get price on iteration {i+1}.[/red]")
            
            if i < iterations - 1:
                time.sleep(self.config.INTERVAL_SECONDS)

        console.print("\n[bold yellow]Data collection finished. Generating visualizers...[/bold yellow]")
        line_path, candle_path = self.visualizer.generate_all_graphs()
        
        if line_path and candle_path:
            self.generate_html_dashboard(max_price, line_path, candle_path)
            
            if self.notifier:
                console.print("[cyan]Sending email report with Line graph...[/cyan]")
                self.notifier.send_email(max_price, line_path)
        
        console.print(Panel.fit("[bold green]System Run Completed Successfully![/bold green]", border_style="green"))
        return max_price