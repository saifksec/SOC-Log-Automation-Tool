# 1. Open and read the file
file = open('auth.log', 'r')
logs = file.readlines()
file.close()

failed_attempts = {}

# 2. Scan line-by-line
for line in logs:
    if "Failed password" in line:
        
        # Split the sentence into words and grab the 11th word (the IP)
        words = line.split()
        ip = words[10]
        
        # Scoreboard logic
        if ip in failed_attempts:
            failed_attempts[ip] += 1
        else:
            failed_attempts[ip] = 1

# 3. Intelligent Alarm Logic
alarm_triggered = False

for ip in failed_attempts:
    count = failed_attempts[ip]
    
    if count >= 5:
        # Only print the big red header ONCE
        if alarm_triggered == False:
            print("🚨 SOC ALARM: BRUTE FORCE DETECTED 🚨")
            print("-----------------------------------")
            alarm_triggered = True
            
        print("Target IP: " + ip + " | Failed Logins: " + str(count))

# If we checked everything and the switch is still False, we are safe
if alarm_triggered == False:
    print("✅ ALL CLEAR: No brute force attacks detected.")