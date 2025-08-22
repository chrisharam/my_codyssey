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
                cpu = os.popen('sysctl -n machdep.cpu.brand_string').read().strip()
                if cpu:
                    info['cpu'] = cpu

                cores = os.popen('sysctl -n hw.ncpu').read().strip()
                if cores:
                    info['cpu_cores'] = cores

                mem_bytes = os.popen('sysctl -n hw.memsize').read().strip()
                if mem_bytes.isdigit():
                    info['memory_gb'] = round(int(mem_bytes) / (1024 ** 3), 2)
            except Exception:
                pass

        elif system == 'Linux':
            try:
                cpu = os.popen("grep 'model name' /proc/cpuinfo | head -1 | cut -d ':' -f2").read().strip()
                if cpu:
                    info['cpu'] = cpu

                cores = os.popen('nproc').read().strip()
                if cores:
                    info['cpu_cores'] = cores

                mem_kb_line = os.popen("grep MemTotal /proc/meminfo").read()
                if mem_kb_line:
                    mem_kb = int(mem_kb_line.split()[1])
                    info['memory_gb'] = round(mem_kb / 1024 / 1024, 2)
            except Exception:
                pass

        print(json.dumps(info, indent=4))
        return info

    def get_cpu_usage_linux(self):
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
                # Get CPU load average (not usage %)
                cpu_load = os.popen('uptime').read()
                load_avg = cpu_load.split('load averages:')[1].strip().split()[0]
                load['cpu_usage_percent'] = load_avg
            except Exception:
                pass
            
            # Get memory usage
            try:
                vm_stat = os.popen('vm_stat').read()
                mem_stats = {}
                page_size = 0
                
                # Extract page size and memory stats from vm_stat output
                for line in vm_stat.split('\n'):
                    if ':' in line:
                        try:
                            key, value = line.split(':')
                            if '(page size' in value:
                                page_size = int(value.split(' ')[3])
                                continue
                            mem_stats[key.strip()] = int(value.strip().strip('.'))
                        except (ValueError, IndexError):
                            continue
                
                if page_size > 0:
                    free_mem = (mem_stats.get('Pages free', 0) + mem_stats.get('Pages inactive', 0)) * page_size
                    total_mem = (mem_stats.get('Pages wired down', 0) + mem_stats.get('Pages active', 0) + free_mem)
                    
                    if total_mem > 0:
                        used_mem_percent = round((total_mem - free_mem) / total_mem * 100, 2)
                        load['memory_usage_percent'] = str(used_mem_percent)
            except Exception:
                pass

        elif system == 'Linux':
            try:
                cpu_usage = self.get_cpu_usage_linux()
                load['cpu_usage_percent'] = str(cpu_usage)
                
                mem_line = os.popen("free | grep Mem").read()
                parts = mem_line.split()
                total = float(parts[1])
                used = float(parts[2])
                mem_percent = round(used / total * 100, 2)
                load['memory_usage_percent'] = str(mem_percent)
            except Exception:
                pass

        print(json.dumps(load, indent=4))
        return load


if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()