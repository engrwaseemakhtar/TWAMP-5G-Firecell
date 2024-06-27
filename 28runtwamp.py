import subprocess
from datetime import datetime
import csv
import re
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats  # Import scipy.stats module

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def run_twampy_command():
    timestamp = get_timestamp()
    output_filename = f"TWAMP_{timestamp}.csv"
    results_folder = "Results"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    
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
    
    # Lists to store values for plotting
    rtt_values = []
    outbound_values = []
    inbound_values = []
    
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
                # Convert values to float (assuming they are in milliseconds)
                rtt_values.append(float(rtt))
                outbound_values.append(float(outbound))
                inbound_values.append(float(inbound))
            else:
                print(f"No match found for line: {line}")
    
    print(f"Results saved to {output_filename}")
    
    # Plot and save CDF and PDF for rtt
    plot_and_save_cdf_and_pdf(rtt_values, "rtt", results_folder, timestamp)
    
    # Plot and save CDF and PDF for outbound
    plot_and_save_cdf_and_pdf(outbound_values, "outbound", results_folder, timestamp)
    
    # Plot and save CDF and PDF for inbound
    plot_and_save_cdf_and_pdf(inbound_values, "inbound", results_folder, timestamp)

def plot_and_save_cdf_and_pdf(data, column_name, results_folder, timestamp):
    plt.figure(figsize=(8, 4))
    
    # Compute CDF
    sorted_data = np.sort(data)
    yvals_cdf = np.arange(len(sorted_data)) / float(len(sorted_data))
    
    # Plot CDF
    plt.subplot(1, 2, 1)
    plt.plot(sorted_data, yvals_cdf)
    plt.xlabel(column_name)
    plt.ylabel("Cumulative Probability")
    plt.title(f"CDF of {column_name}")
    plt.grid(True)
    
    # Compute PDF
    density = stats.gaussian_kde(sorted_data)
    xvals_pdf = np.linspace(min(sorted_data), max(sorted_data), 1000)
    yvals_pdf = density(xvals_pdf)
    
    # Plot PDF
    plt.subplot(1, 2, 2)
    plt.plot(xvals_pdf, yvals_pdf)
    plt.xlabel(column_name)
    plt.ylabel("Probability Density")
    plt.title(f"PDF of {column_name}")
    plt.grid(True)
    
    # Save combined plot as PNG
    combined_png_file = os.path.join(results_folder, f"{column_name}_{timestamp}_combined.png")
    plt.savefig(combined_png_file)
    
    # Save CDF plot as PNG
    cdf_png_file = os.path.join(results_folder, f"{column_name}_{timestamp}_cdf.png")
    plt.subplot(1, 2, 1)
    plt.savefig(cdf_png_file)
    
    # Save PDF plot as PNG
    pdf_png_file = os.path.join(results_folder, f"{column_name}_{timestamp}_pdf.png")
    plt.subplot(1, 2, 2)
    plt.savefig(pdf_png_file)
    
    # Save combined plot as PDF
    combined_pdf_file = os.path.join(results_folder, f"{column_name}_{timestamp}_combined.pdf")
    plt.savefig(combined_pdf_file, format='pdf')
    
    # Close plot
    plt.close()

if __name__ == "__main__":
    run_twampy_command()

