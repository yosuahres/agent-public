import pandas as pd
from transformers import pipeline
CSV_FILE_PATH = "/Users/hares/Desktop/infor2025/robot/agentllm/data-csv/class.csv"

def generate_report(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)

        if df.empty:
            return "No data found in the CSV file."

        text_generator = pipeline("text-generation", model="gpt2")

        report = text_generator(f"Generate a report based on the following data: {df.to_string()}",
                                max_length=500,
                                num_return_sequences=1)[0]['generated_text']

        return report
    except FileNotFoundError:
        return f"Error: CSV file not found at {csv_file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def run_report_generation():
    report = generate_report(CSV_FILE_PATH)
    print(report)

if __name__ == "__main__":
    print("Agent LLM is running. It will generate a report whenever data is available.")
    while True:
        try:
            run_report_generation()
        except Exception as e:
            print(f"An error occurred: {e}")
