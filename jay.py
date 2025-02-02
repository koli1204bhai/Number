import random
import time
import sys
import threading
import datetime
import pytz
from colorama import Fore, Style, init
import pyfiglet
import shutil

# Initialize colorama for Windows support
init(autoreset=True)

# Predefined results with colors
results = [
    (Fore.RED + "BIG  7/9"),
    (Fore.BLUE + "SMALL  1/4"),
    (Fore.GREEN + "SMALL  2/3"),
    (Fore.YELLOW + "BIG  5/8"),
    (Fore.CYAN + "BIG  6/7"),
    (Fore.MAGENTA + "SMALL  2/4")
]

# Store history
history = []

# Function to print large, bold text once
def print_large_text(text, color=Fore.WHITE):
    figlet_text = pyfiglet.figlet_format(text)
    print(color + figlet_text + Style.RESET_ALL)

# Function for horizontal loading animation
def loading_animation():
    sys.stdout.write(Fore.LIGHTWHITE_EX + "Processing: ")
    sys.stdout.flush()
    for i in range(1, 11):  # 10-step progress bar
        time.sleep(0.3)
        sys.stdout.write(Fore.GREEN + "█")
        sys.stdout.flush()
    print("\n")

# Function to update the period number and countdown
def update_timer():
    global win30sec_period
    utc_now = datetime.datetime.now(pytz.utc)
    
    seconds = utc_now.second
    minutes = utc_now.minute
    hours = utc_now.hour

    # Calculate the correct period number for 30-second intervals
    total_periods = hours * 120 + minutes * 2 + (1 if seconds >= 30 else 0)
    total_periods += 1  # Adjust if needed

    # Calculate remaining seconds in the current 30-second interval
    remaining_seconds = 30 - (seconds % 30)

    # Format the period number correctly
    period_number = f"{100050000 + total_periods:04d}"
    date_str = utc_now.strftime("%Y%m%d")

    win30sec_period = date_str + period_number
    win30sec_second = f"00:{remaining_seconds:02d}"

    # Print period number in one place
    terminal_width = shutil.get_terminal_size().columns
    period_text = f"PERIOD: {win30sec_period} | TIMER: {win30sec_second}"
    sys.stdout.write("\r" + Fore.YELLOW + Style.BRIGHT + period_text.center(terminal_width) + Style.RESET_ALL)
    sys.stdout.flush()

    # Automatically generate result when the timer reaches 00:00
    if remaining_seconds == 30:
        generate_result(win30sec_period)

    # Schedule the function to run again after 1 second
    threading.Timer(1, update_timer).start()

# Function to generate a random result and store it in history
def generate_result(period):
    loading_animation()

    result = random.choice(results)
    history.append(f"Period: {period} → {result}")

    # Display result in center
    terminal_width = shutil.get_terminal_size().columns
    result_text = f"★ RESULT: {result} ★"
    print("\n" + Fore.LIGHTGREEN_EX + result_text.center(terminal_width) + Style.RESET_ALL)

    # Save history to a file
    with open("history.txt", "a") as file:
        file.write(f"{period} - {result}\n")

    # Display last 5 history results
    print(Fore.LIGHTWHITE_EX + "-" * terminal_width)
    print(Fore.LIGHTMAGENTA_EX + "★ HISTORY ★\n")
    for h in history[-5:]:
        print(Fore.LIGHTWHITE_EX + h.center(terminal_width))
    print(Fore.LIGHTWHITE_EX + "-" * terminal_width + "\n")

# Main function to start the timer
def main():
    print_large_text("JAY BABA", Fore.LIGHTGREEN_EX)  # Show only once at the start
    print(Fore.LIGHTCYAN_EX + "★ Welcome to Hack  { Developer = JAY BABA} ★")
    print(Fore.LIGHTWHITE_EX + "-" * shutil.get_terminal_size().columns)

    # Start the period timer
    update_timer()

# Run the script
if __name__ == "__main__":
    main()
