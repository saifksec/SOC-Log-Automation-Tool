# SOC-Log-Automation-Tool

Objective: A Python-based automation script designed to parse Linux auth.log files, track failed SSH login attempts, and automatically flag IP addresses breaching the brute-force threshold.

Tools Used: Python, Kali Linux, Hydra, Metasploitable.

### Phase 1: The Attack (Red Team)
To validate the tool, I generated real attack traffic using Hydra to launch an SSH brute-force attack against a vulnerable local server. 

<img width="1149" height="392" alt="Screenshot 2026-05-25 035754" src="https://github.com/user-attachments/assets/b63bbe74-8767-4932-b9cb-1c4d69fbaf4e" />


### Phase 2: The Evidence (Log Extraction)
Following the attack, I securely extracted the auth.log file over the network. As seen below, manually reviewing thousands of lines of raw system logs is highly inefficient for a SOC team.
<img width="1047" height="218" alt="Screenshot 2026-05-25 040013" src="https://github.com/user-attachments/assets/0d7ab0ad-81e6-4bd8-b2a4-df2d50c974b3" />
<img width="1269" height="1015" alt="Screenshot 2026-05-25 175453" src="https://github.com/user-attachments/assets/c0e9bc33-56e7-45e1-96f2-32c5e0ef164a" />



### Phase 3: The Detection (Blue Team Automation)
To triage the aftermath, I ran the custom Python parser. The script successfully chewed through the raw logs, extracted the IPs, tracked the failure counts, and triggered a SOC alarm for the exact attacker IP.

<img width="806" height="188" alt="Screenshot 2026-05-25 040218" src="https://github.com/user-attachments/assets/c35b1927-ad90-44b6-8cf3-7c4fe56dd83d" />


---

###  Challenges Encountered & Troubleshooting

The Problem: Cryptographic Deprecation (Legacy SSH Protocols)
During the lab execution, my modern attacker machine (Kali Linux) and my host machine (Windows) both actively refused to connect to the victim machine (Metasploitable 2) over SSH. I received kex error : no match for method mac algo and no matching host key type found errors.

The Root Cause:
Modern operating systems are configured with strict security baselines out-of-the-box and actively block legacy, insecure encryption algorithms (like ssh-rsa and hmac-md5). Metasploitable 2 is an intentionally vulnerable legacy server, so the modern machines refused to lower their security standards to communicate with it.

The Engineering Solutions:
To successfully execute the attack and extract the forensic data, I had to deliberately force my modern tools to accept legacy protocols:

1. Kali Linux (The Attacker): I utilized the kali-tweaks command-line utility, navigated to the Hardening menu, and enabled Wide Compatibility for the SSH client. This allowed Hydra to successfully negotiate the connection and brute-force the server.
2. Windows Host (The Defender): To securely extract the auth.log file over the network, I had to bypass Windows' strict SSH key checking. I added a specific parameter to my Secure Copy command to temporarily allow legacy RSA keys: scp -o HostKeyAlgorithms=+ssh-rsa msfadmin@[TARGET_IP]:/var/log/auth.log ./auth.log
