import tkinter as tk
from threading import Thread
import time
from datetime import datetime
import requests
import re
import pygetwindow as gw

appsToTrack = ["Word", "Excel", "Outlook", "PowerPoint", "Calendar", ".pdf", "Adobe Acrobat Reader (64-bit)"]

class ActivityTrackerApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Activity Tracker")

        self.tracked_data_label = tk.Label(root, text="Tracked Data", font=('Arial', 14, 'bold'))
        self.tracked_data_label.pack(pady=(10, 5))

        self.tracked_data_text = tk.Text(root, wrap=tk.WORD, font=('Arial', 12), spacing1=3, spacing2=2, spacing3=2)
        self.tracked_data_text.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)
        self.tracked_data_text.pack_propagate(0)  # Prevent the widget from affecting its parent's size

        # Set the initial tracked data
        self.tracked_data = "Activity Tracker is running...\n"
        self.window_count = 1

        # Initialize the last known active window
        self.last_active_window = self.get_active_window_title()

        # Start the tracking function in a separate thread
        self.tracking_thread = Thread(target=self.track_activity, daemon=True)
        self.tracking_thread.start()

        # Schedule the update on the main thread
        self.root.after(1, self.update_tracked_data)
        self.start_time = datetime.now()

    def extract_application_name(self, window_title):
        # Use regular expression to split by '-', '/', '\', or '|'
        parts = re.split(r'[-/\\|]', window_title)
        # Take the last part as the application name
        return parts[-1].strip() if parts else window_title.strip()

    def post_data_to_api(self, data):
        api_url = "http://125.63.88.147:7401/api/PostData/InsertData"
        headers = {
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(api_url, json=data, headers=headers)

            if response.status_code == 200:
                print("POST request successful!")
                print("Status Code:", response.status_code)
                print("Response:", response.json())
            else:
                print("POST request failed with status code:", response.status_code)
                print("Response:", response.text)

        except requests.RequestException as e:
            print("An error occurred while making the POST request:", str(e))

    def track_activity(self):
        try:
            while True:
                active_window = self.get_active_window_title()

                if active_window and active_window != self.last_active_window:
                    tracked_data = f"{self.window_count}. Active Window: {active_window}\n"

                    # Set the tracked data in the instance variable
                    self.tracked_data += tracked_data
                    self.window_count += 1

                    # Update the last known active window
                    self.last_active_window = active_window

                    # Post data to API
                    app_name = self.extract_application_name(active_window)
                    if app_name and any(app in app_name for app in appsToTrack):
                        self.post_data_to_api({
                            "applicationName": app_name,
                            "titleName": active_window,
                            "startDate": self.start_time.isoformat(),
                            "endDate": datetime.now().isoformat()
                        })
                        self.start_time = datetime.now()
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def update_tracked_data(self):
        # Update the text widget with the tracked data
        self.tracked_data_text.config(state=tk.NORMAL)
        self.tracked_data_text.delete(1.0, tk.END)
        self.tracked_data_text.insert(tk.END, self.tracked_data)
        self.tracked_data_text.config(state=tk.DISABLED)

        # Schedule the update on the main thread again
        self.root.after(1000, self.update_tracked_data)

    def get_active_window_title(self):
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                return active_window.title
        except Exception as e:
            print(f"Error getting active window: {e}")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    username = "username"
    app = ActivityTrackerApp(root, username)
    root.mainloop()
