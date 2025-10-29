#!/usr/bin/env python3
"""
Export all Prometheus data to CSV
Combines house, weather, and inverter sensor data by timestamp
"""

import os
import glob
import re
from datetime import datetime
from collections import defaultdict
import csv

def parse_prometheus_file(filepath):
    """Parse a Prometheus file and return timestamp and metrics"""
    data = {}
    
    # Extract timestamp from filename: sensor-YYYYMMDD_HHMMSS.prom
    filename = os.path.basename(filepath)
    match = re.search(r'(\d{8}_\d{6})\.prom', filename)
    if match:
        timestamp_str = match.group(1)
        try:
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
        except:
            # Fallback to file mtime
            timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))
    else:
        timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))
    
    # Read metrics from file
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Parse: metric_name{labels} value
                    if '{' in line and '}' in line:
                        metric_part = line.split('{')[0]
                        value_part = line.split('}')[1].strip()
                        try:
                            value = float(value_part)
                            data[metric_part] = value
                        except ValueError:
                            continue
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    
    return timestamp, data

def main():
    prometheus_dir = "/home/constantine/mpp-solar/prometheus"
    output_file = "/home/constantine/prometheus_export.csv"
    
    print("Exporting Prometheus data to CSV...")
    print(f"Source: {prometheus_dir}")
    print(f"Output: {output_file}")
    
    # Collect all data organized by timestamp
    all_data = defaultdict(dict)
    all_metrics = set()
    
    # Process all .prom files
    file_patterns = [
        "house-*.prom",
        "weather-*.prom",
        "mpp-solar-inverter-qpigs*.prom"
    ]
    
    total_files = 0
    for pattern in file_patterns:
        files = glob.glob(os.path.join(prometheus_dir, pattern))
        print(f"Processing {len(files)} files matching {pattern}...")
        
        for filepath in files:
            timestamp, metrics = parse_prometheus_file(filepath)
            
            # Merge metrics for this timestamp
            all_data[timestamp].update(metrics)
            all_metrics.update(metrics.keys())
            total_files += 1
            
            if total_files % 100 == 0:
                print(f"  Processed {total_files} files...")
    
    print(f"\nTotal files processed: {total_files}")
    print(f"Unique timestamps: {len(all_data)}")
    print(f"Unique metrics: {len(all_metrics)}")
    
    # Sort metrics for consistent column order
    sorted_metrics = sorted(all_metrics)
    
    # Write to CSV
    print(f"\nWriting CSV to {output_file}...")
    with open(output_file, 'w', newline='') as csvfile:
        # Create header
        fieldnames = ['timestamp'] + sorted_metrics
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Sort by timestamp and write rows
        for timestamp in sorted(all_data.keys()):
            row = {'timestamp': timestamp.isoformat()}
            row.update(all_data[timestamp])
            writer.writerow(row)
    
    # Print summary
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
    print(f"\n✓ Export complete!")
    print(f"  File: {output_file}")
    print(f"  Size: {file_size:.2f} MB")
    print(f"  Rows: {len(all_data) + 1} (including header)")
    print(f"  Columns: {len(sorted_metrics) + 1} (timestamp + {len(sorted_metrics)} metrics)")
    
    # Show sample of metrics
    print(f"\nSample metrics included:")
    for metric in sorted_metrics[:10]:
        print(f"  - {metric}")
    if len(sorted_metrics) > 10:
        print(f"  ... and {len(sorted_metrics) - 10} more")

if __name__ == '__main__':
    main()
