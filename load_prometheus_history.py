#!/usr/bin/env python3
"""
Load historical data from Prometheus files into memory
"""
import os
import glob
import re
from datetime import datetime
import logging

def parse_prometheus_file_with_timestamp(file_path):
    """Parse a Prometheus file and extract metrics with file modification time as timestamp"""
    data = {}
    try:
        # Get file modification time as timestamp
        file_mtime = os.path.getmtime(file_path)
        timestamp = datetime.fromtimestamp(file_mtime).isoformat()
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Parse each metric line
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Parse Prometheus metric format: metric_name{labels} value
                if '{' in line and '}' in line:
                    metric_part = line.split('{')[0]
                    value_part = line.split('}')[1].strip()
                    
                    try:
                        value = float(value_part)
                        data[metric_part] = value
                    except ValueError:
                        continue
        
        # Add timestamp to the data
        if data:
            data['timestamp'] = timestamp
                        
    except Exception as e:
        logging.error(f"Error parsing Prometheus file {file_path}: {e}")
    
    return data

def load_historical_prometheus_data(prometheus_dir, max_entries=1000):
    """
    Load historical data from Prometheus files
    Returns a list of historical entries
    """
    historical_data = []
    
    try:
        # Get all .prom files sorted by modification time
        prom_files = glob.glob(os.path.join(prometheus_dir, "mpp-solar-inverter-qpigs*.prom"))
        
        # Sort by modification time (oldest first)
        prom_files.sort(key=lambda x: os.path.getmtime(x))
        
        # Take the last max_entries files
        prom_files = prom_files[-max_entries:] if len(prom_files) > max_entries else prom_files
        
        for file_path in prom_files:
            data = parse_prometheus_file_with_timestamp(file_path)
            if data and 'timestamp' in data:
                historical_data.append(data)
        
        logging.info(f"Loaded {len(historical_data)} historical entries from Prometheus files")
                        
    except Exception as e:
        logging.error(f"Error loading historical Prometheus data: {e}")
    
    return historical_data

if __name__ == '__main__':
    # Test loading
    import sys
    logging.basicConfig(level=logging.INFO)
    
    prometheus_dir = "/home/constantine/mpp-solar/prometheus"
    data = load_historical_prometheus_data(prometheus_dir)
    
    print(f"Loaded {len(data)} entries")
    if data:
        print(f"First entry timestamp: {data[0].get('timestamp')}")
        print(f"Last entry timestamp: {data[-1].get('timestamp')}")
        print(f"Sample metrics: {list(data[0].keys())[:5]}")
