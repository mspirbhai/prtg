import json
import re
import subprocess

result = {}

result.update({"prtg":{"result":[]}})

data = []

host = "www.google.com"

ping = subprocess.Popen(
    ["ping","/n", "10", host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

out, error = ping.communicate()

if len(error) == 0:
    
    # Use regex to find the packet loss percentage
    packet_loss_pattern = r'Lost = (\d+) \((\d+)% loss\)'
    packet_loss_match = re.search(packet_loss_pattern, str(out))

    if packet_loss_match:
        lost_packets = packet_loss_match.group(1)
        packet_loss_percentage = packet_loss_match.group(2)

    # Use regex to find min, avg, and max rtt times
    # Use regex to find min, avg, and max RTT times
    rtt_pattern = r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms'
    rtt_match = re.search(rtt_pattern, str(out))

    if rtt_match:
        min_rtt = rtt_match.group(1)
        max_rtt = rtt_match.group(2)
        avg_rtt = rtt_match.group(3)

    data.append(dict(Channel = "Packet Loss",
                Value = int(packet_loss_percentage),
                Unit = "Percent"))
    data.append(dict(Channel = "Minimum",
                Value = int(min_rtt),
                CustomUnit = "ms"))
    data.append(dict(Channel = "Average",
                Value = int(avg_rtt),
                CustomUnit = "ms"))
    data.append(dict(Channel = "Maximum",
                Value = int(max_rtt),
                CustomUnit = "ms"))

result["prtg"]["result"] += data


print(json.dumps(result,indent=4))
