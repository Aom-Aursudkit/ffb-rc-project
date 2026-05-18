import socket
import time
import csv
import os

ESP32_IP = "192.168.4.1"
PORT = 4210
FILENAME = "latency_results.csv"
MAX_PACKETS = 100 # Target count of successful packets

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5)

results = []
packets_sent = 0

print(f"Starting test. Targeting {MAX_PACKETS} successful packets.")
print(f"Saving data to {FILENAME}.")

# Initialize CSV
file_exists = os.path.isfile(FILENAME)
with open(FILENAME, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Timestamp", "Latency_ms"])

    # Run until we get 100 successful packets
    while len(results) < MAX_PACKETS:
        start_time = time.time()
        message = f"{start_time}".encode()
        sock.sendto(message, (ESP32_IP, PORT))
        packets_sent += 1

        try:
            data, addr = sock.recvfrom(1024)
            end_time = time.time()
            rtt_ms = (end_time - start_time) * 1000
            
            writer.writerow([time.strftime("%H:%M:%S"), f"{rtt_ms:.2f}"])
            
            results.append(rtt_ms)
            print(f"Received {len(results)}/{MAX_PACKETS}: {rtt_ms:.2f} ms")
            
        except socket.timeout:
            print(f"Packet {packets_sent}: Lost!")

        time.sleep(0.1) # Small delay to avoid flooding the ESP32

# Final Summary
print(f"\n--- Summary ---")
print(f"Packets received: {len(results)}")
print(f"Total attempts: {packets_sent}")
print(f"Packet Loss Rate: {((packets_sent - len(results)) / packets_sent) * 100:.2f}%")
print(f"Average Latency: {sum(results)/len(results):.2f} ms")
print(f"Min Latency: {min(results):.2f} ms")
print(f"Max Latency: {max(results):.2f} ms")

sock.close()
