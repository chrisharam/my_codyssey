import os
import platform
import json
import time

class MissionComputer:
    def __init__(self):
        pass

    def get_mission_computer_info(self):
        """
        Retrieves and prints basic system information (OS, CPU, Memory).
        """
        system = platform.system()
        info = {
            'os': system,
            'os_version': platform.version(),
            'cpu': 'unknown',
            'cpu_cores': 'unknown',
            'memory_gb': 'unknown'
        }

        if system == 'Darwin':  # macOS
            try:
                # Get CPU brand string
                cpu_brand = os.popen('sysctl -n machdep.cpu.brand_string').read().strip()
                if cpu_brand:
                    info['cpu'] = cpu_brand
                
                # Get number of CPU cores
                cpu_cores = os.popen('sysctl -n hw.ncpu').read().strip()
                if cpu_cores:
                    info['cpu_cores'] = int(cpu_cores)
                
                # Get total physical memory in GB
                mem_bytes = os.popen('sysctl -n hw.memsize').read().strip()
                if mem_bytes.isdigit():
                    info['memory_gb'] = round(int(mem_bytes) / (1024**3), 2)
            except Exception:
                pass

        elif system == 'Linux':
            try:
                # Get CPU model name
                cpu_model = os.popen("grep 'model name' /proc/cpuinfo | head -1 | cut -d ':' -f2").read().strip()
                if cpu_model:
                    info['cpu'] = cpu_model
                
                # Get number of CPU cores
                cpu_cores = os.popen('nproc').read().strip()
                if cpu_cores:
                    info['cpu_cores'] = int(cpu_cores)

                # Get total physical memory in GB
                mem_kb_line = os.popen("grep MemTotal /proc/meminfo").read()
                if mem_kb_line:
                    mem_kb = int(mem_kb_line.split()[1])
                    info['memory_gb'] = round(mem_kb / 1024 / 1024, 2)
            except Exception:
                pass

        print(json.dumps(info, indent=4))
        return info

    def get_cpu_usage_linux(self):
        """
        Calculates and returns real-time CPU usage on Linux.
        """
        try:
            with open('/proc/stat', 'r') as f:
                line = f.readline()
            parts = line.split()
            total_time_1 = sum(map(int, parts[1:]))
            idle_time_1 = int(parts[4])

            time.sleep(1)

            with open('/proc/stat', 'r') as f:
                line = f.readline()
            parts = line.split()
            total_time_2 = sum(map(int, parts[1:]))
            idle_time_2 = int(parts[4])

            total_diff = total_time_2 - total_time_1
            idle_diff = idle_time_2 - idle_time_1
            usage = 100 * (total_diff - idle_diff) / total_diff
            return round(usage, 2)
        except Exception:
            return 'unknown'
            
    def get_mission_computer_load(self):
        """
        Retrieves and prints system load (CPU and Memory usage).
        """
        system = platform.system()
        load = {
            'cpu_usage_percent': 'unknown',
            'memory_usage_percent': 'unknown'
        }

        if system == 'Darwin':  # macOS
            try:
                # Get real-time CPU usage with 'top' command
                cpu_info = os.popen("top -l 1 | grep 'CPU usage'").read()
                if cpu_info:
                    idle_percent = float(cpu_info.split(',')[2].strip().replace('idle', '').replace('%', ''))
                    cpu_usage_percent = 100 - idle_percent
                    load['cpu_usage_percent'] = round(cpu_usage_percent, 2)

                # Get real-time memory usage
                vm_stat = os.popen('vm_stat').read()
                page_size_line = os.popen('sysctl -n vm.pagesize').read().strip()
                if page_size_line:
                    page_size = int(page_size_line)
                    pages_free = int(os.popen("vm_stat | grep 'Pages free' | awk '{print $3}'").read().strip().replace('.', ''))
                    pages_active = int(os.popen("vm_stat | grep 'Pages active' | awk '{print $3}'").read().strip().replace('.', ''))
                    pages_inactive = int(os.popen("vm_stat | grep 'Pages inactive' | awk '{print $3}'").read().strip().replace('.', ''))
                    pages_speculative = int(os.popen("vm_stat | grep 'Pages speculative' | awk '{print $3}'").read().strip().replace('.', ''))
                    pages_wired = int(os.popen("vm_stat | grep 'Pages wired down' | awk '{print $4}'").read().strip().replace('.', ''))
                    
                    total_pages = pages_free + pages_active + pages_inactive + pages_speculative + pages_wired
                    used_pages = pages_active + pages_wired
                    
                    if total_pages > 0:
                        used_mem_percent = round((used_pages / total_pages) * 100, 2)
                        load['memory_usage_percent'] = used_mem_percent
            except Exception as e:
                pass

        elif system == 'Linux':
            try:
                # Get CPU usage
                cpu_usage = self.get_cpu_usage_linux()
                load['cpu_usage_percent'] = cpu_usage
                
                # Get memory usage
                mem_line = os.popen("free | grep Mem").read()
                parts = mem_line.split()
                total = float(parts[1])
                used = float(parts[2])
                mem_percent = round(used / total * 100, 2)
                load['memory_usage_percent'] = mem_percent
            except Exception:
                pass

        print(json.dumps(load, indent=4))
        return load

if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()