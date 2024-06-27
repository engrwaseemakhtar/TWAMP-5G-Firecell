import subprocess
from datetime import datetime
import csv
import re

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def run_twampy_command():
    timestamp = get_timestamp()
    output_filename = f"TWAMP_{timestamp}.csv"
    
    command = ["sudo", "python3", "twampy.py", "sender", "-i", "100", "-c", "100", "16.170.229.66:862"]
    
    # Run the command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print(f"Error occurred: {result.stderr}")
        return
    
    # Define the column headers
    headers = ["rseq", "sseq", "rtt", "outbound", "inbound"]
    
    # Regular expression pattern to extract numeric values
    pattern = re.compile(r"rseq=(\d+)\s+sseq=(\d+)\s+rtt=([\d.]+)ms\s+outbound=([\d.]+)ms\s+inbound=([\d.]+)ms")
    
    # Parse the output and write to CSV
    with open(output_filename, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(headers)  # Write the headers
        
        for line in result.stdout.splitlines():
            # Skip lines containing the unwanted text
            if "asso" in line:
                continue

            # Match the line with the regular expression
            match = pattern.search(line)
            if match:
                # Extract the matched groups
                rseq, sseq, rtt, outbound, inbound = match.groups()
                # Write the values to the CSV file
                csv_writer.writerow([rseq, sseq, rtt, outbound, inbound])
            else:
                print(f"No match found for line: {line}")
    
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    run_twampy_command()

