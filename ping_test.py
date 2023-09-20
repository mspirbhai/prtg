import re
import subprocess

from paesslerag_prtg_sensor_api.sensor.result import CustomSensorResult
from paesslerag_prtg_sensor_api.sensor.units import ValueUnit

if __name__ == "__main__":
    try:

        host = "www.google.com"
        ping_number_times = "10"

        ping = subprocess.Popen(
            ["ping","/n", ping_number_times, host],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        out, error = ping.communicate()

        if len(error) == 0:
            
            # Use regex to find the packet loss percentage

            csr = CustomSensorResult(text="This sensor runs on TZARUPROBE03")
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

            csr.add_primary_channel(name = "Packet Loss",
                                    value = int(packet_loss_percentage),
                                    unit = ValueUnit.PERCENT,
                                    is_float=False,
                                    is_limit_mode=True,
                                    limit_max_error=2,
                                    limit_error_msg="Packet loss too high")
            csr.add_channel(name = "Minimum",
                            value = int(min_rtt),
                            unit = ValueUnit.CUSTOM)
            csr._channels[-1]["CustomUnit"] = "ms"
                            
            csr.add_channel(name = "Average",
                            value = int(avg_rtt),
                            unit = ValueUnit.CUSTOM)
            csr._channels[-1]["CustomUnit"] = "ms"
            
            csr.add_channel(name = "Maximum",
                            value = int(max_rtt),
                            unit = ValueUnit.CUSTOM,
                            limit_max_error=300,
                            limit_error_msg="Latency too high")
            csr._channels[-1]["CustomUnit"] = "ms"
            
        print(csr.json_result)

    except Exception as e:
        csr = CustomSensorResult(text="Python Script execution error")
        csr.error = "Python Script execution error: %s" % str(e)
        print(csr.json_result)