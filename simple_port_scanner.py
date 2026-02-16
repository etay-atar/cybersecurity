#!/usr/bin/env python3
import socket
import sys
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import init, Fore, Style
import pyfiglet

# Initialize colorama
init(autoreset=True)

def print_banner():
    ascii_banner = pyfiglet.figlet_format("Port Scanner")
    print(Fore.CYAN + ascii_banner)
    print(Fore.BLUE + "=" * 60)
    print(Fore.BLUE + "    Multi-Threaded Port Scanner v 1.0")
    print(Fore.BLUE + "=" * 60 + "\n")

def get_host_ip(host_name):
    try:
        host_ip = socket.gethostbyname(host_name)
        return host_ip
    except socket.gaierror:
        return None

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        s.close()
        if result == 0:
            return port
    except Exception:
        pass
    return None

def scan_ports_generator(target, start_port, end_port, threads):
    """
    Generator that yields scan progress and results.
    Yields dictionaries: 
    - {'type': 'progress', 'current': n, 'total': m}
    - {'type': 'result', 'port': p}
    - {'type': 'complete', 'duration': d, 'open_ports': []}
    """
    start_time = time.time()
    ports = range(start_port, end_port + 1)
    total_ports = len(ports)
    completed_ports = 0
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            completed_ports += 1
            
            # Yield progress
            yield {'type': 'progress', 'current': completed_ports, 'total': total_ports}
            
            try:
                result = future.result()
                if result:
                    open_ports.append(result)
                    yield {'type': 'result', 'port': result}
            except Exception:
                pass

    end_time = time.time()
    duration = end_time - start_time
    yield {'type': 'complete', 'duration': duration, 'open_ports': sorted(open_ports)}

def scan_ports(target, start_port, end_port, threads):
    """
    CLI wrapper for the scan generator.
    """
    print(f"Target: {Fore.GREEN}{target}{Style.RESET_ALL} | Ports: {start_port}-{end_port} | Threads: {threads}")
    
    # We need to manually handle the tqdm progress bar here since we are consuming a generator
    total_ports = end_port - start_port + 1
    pbar = tqdm(total=total_ports, desc="Scanning", unit="port")
    
    open_ports = []
    duration = 0
    
    for event in scan_ports_generator(target, start_port, end_port, threads):
        if event['type'] == 'progress':
            pbar.update(event['current'] - pbar.n)
        elif event['type'] == 'result':
            # port = event['port']
            # tqdm.write(f"{Fore.GREEN}[+] Port {port} is open{Style.RESET_ALL}")
            pass
        elif event['type'] == 'complete':
            open_ports = event['open_ports']
            duration = event['duration']
            
    pbar.close()

    print("\n" + Fore.BLUE + "=" * 60)
    print(f"Scan completed in {Fore.CYAN}{duration:.2f}{Style.RESET_ALL} seconds.")
    
    if open_ports:
        print(f"Found {len(open_ports)} open ports:")
        for port in open_ports:
            print(f"  {Fore.GREEN}[+] Port {port} is open{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No open ports found.{Style.RESET_ALL}")
    print(Fore.BLUE + "=" * 60)

import concurrent.futures

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A fast multi-threaded port scanner.")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("start_port", type=int, help="Start port number")
    parser.add_argument("end_port", type=int, help="End port number")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    
    args = parser.parse_args()
    
    print_banner()
    
    target_ip = get_host_ip(args.target)
    
    if target_ip is None:
        print(f"{Fore.RED}Error: Could not resolve host {args.target}{Style.RESET_ALL}")
        sys.exit(1)
        
    print(f"Resolved {args.target} to {target_ip}\n")
    
    try:
        scan_ports(target_ip, args.start_port, args.end_port, args.threads)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Scan interrupted by user.{Style.RESET_ALL}")
        sys.exit(0)
