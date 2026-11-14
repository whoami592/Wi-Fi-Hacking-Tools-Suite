# 📡 Wi-Fi Hacking Tools Suite

A Python-based, menu-driven Wi-Fi security testing suite for Linux. It wraps common wireless auditing utilities (`nmcli`, `iw`, `aircrack-ng` suite) into a single interactive CLI for scanning networks, testing deauthentication resilience, capturing WPA handshakes, and running dictionary attacks against captured handshakes.

```
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
```

**Coded by Cyber Security Engineer: Mr. Sabaz Ali Khan**

---

## ⚠️ Legal & Ethical Use Only

This tool performs **active wireless attacks** (deauthentication, handshake capture, offline password cracking). These actions are illegal in most countries unless performed on a network you **own** or have **explicit written authorization** to test.

- Use only on your own Wi-Fi infrastructure or in a lab you control.
- If testing for a client/employer, obtain signed authorization before use.
- The author and contributors accept no liability for misuse of this tool.
- Unauthorized access to computer networks is a criminal offense under laws such as Pakistan's PECA 2016, the U.S. CFAA, and equivalent legislation elsewhere.

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Network Scanning** | Lists nearby Wi-Fi networks (SSID, signal strength, security type, channel) via `nmcli`. |
| 2 | **Deauthentication Test** | Sends deauth frames to a target AP using `aireplay-ng` to test client disconnection resilience. |
| 3 | **Handshake Capture** | Captures the WPA 4-way handshake for a chosen network using `airodump-ng`. |
| 4 | **WPA Password Cracking** | Runs an offline dictionary attack against a captured `.pcap` handshake using `aircrack-ng`. |
| 5 | **Monitor Mode Helpers** | Enable/restore monitor mode on a wireless interface via `iw` / `ip`. |
| 6 | **Colorized CLI Menu** | Interactive, color-coded terminal menu for all operations. |

---

## 📋 Requirements

### System
- Linux (tested on Debian/Ubuntu/Kali-based distributions)
- A wireless adapter that supports **monitor mode** and **packet injection**
- Root privileges (the script requires `sudo`)

### Software / Tools
- Python 3.6+
- [`aircrack-ng` suite](https://www.aircrack-ng.org/) (`airmon-ng`, `airodump-ng`, `aireplay-ng`, `aircrack-ng`)
- `network-manager` (`nmcli`)
- `iw`, `iproute2` (`ip`)
- A wordlist for cracking, e.g. `rockyou.txt`

### Install dependencies (Debian/Kali)
```bash
sudo apt update
sudo apt install -y aircrack-ng network-manager iw iproute2 python3
```

---

## 🚀 Installation

```bash
git clone https://github.com/whoami592/Wi-Fi-Hacking-Tools-Suite.git
cd wifi-hacking-tools-suite
chmod +x wifi_hacking_tools_suite.py
```

---

## ▶️ Usage

Run the tool as root (required for interface/mode control and packet injection):

```bash
sudo python3 wifi_hacking_tools_suite.py
```

### Main Menu
```
1. Scan Networks
2. Deauth Attack
3. Capture Handshake
4. Crack WPA Password
5. Exit
```

1. **Scan Networks** — select your wireless interface and view nearby APs sorted by signal strength.
2. **Deauth Attack** — select a target network and attack duration; sends deauth frames via `aireplay-ng`.
3. **Capture Handshake** — select a target network; captures traffic with `airodump-ng` and saves a `.pcap` file. Press `Ctrl+C` to stop capture.
4. **Crack WPA Password** — select a captured `.pcap` file and a wordlist; runs `aircrack-ng` to attempt an offline dictionary attack.
5. **Exit** — quits the tool.

---

## 📁 Output Files

- Handshake captures are saved as `capture_<SSID>_<timestamp>.pcap` in the working directory.
- Cracking results (if found) are printed to the terminal.

---

## 🛠️ Troubleshooting

| Issue | Possible Fix |
|---|---|
| "This tool requires root privileges" | Run with `sudo python3 wifi_hacking_tools_suite.py` |
| No interfaces found | Confirm your adapter is detected: `nmcli device status` |
| Deauth/capture fails | Confirm your adapter supports monitor mode & injection: `airmon-ng` |
| Cracking never finds password | Try a larger/better wordlist; WPA passwords outside the wordlist cannot be found |

---

## 📜 License

This project is released for educational and authorized security-testing purposes only. Add your preferred license (e.g., MIT) here.

---

## 👤 Credit

**Coded by Cyber Security Engineer: Mr. Sabaz Ali Khan**
