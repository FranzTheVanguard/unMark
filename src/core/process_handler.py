import psutil
import win32serviceutil
import win32service

class ProcessHandler:
    def __init__(self):
        self.target_processes = [
            "DSH_Loader.exe",
            "DSH_Loader64.exe",
            "DSH_Service64.exe",
            "DSU_ServiceV6.exe",
            "IMGSF50Start_x64.exe",
            "IMGSF50Start_x86.exe",
            "IMGSF50Svc.exe",
            "PolicyServerService.exe"
        ]
        
        self.target_services = [
            "DSv4_DRM_Control",
            "PolicyServerService",
            "IMGSF50_Svc",
            "LiveUpdate Service V6"
        ]
    
    def find_processes(self):
        found_processes = []
        for proc in psutil.process_iter(['name', 'pid', 'username', 'memory_info']):
            try:
                if proc.info['name'] in self.target_processes:
                    found_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return found_processes

    def terminate_processes(self):
        processes = self.find_processes()
        results = []
        for proc in processes:
            try:
                proc.terminate()
                results.append((proc.info['name'], "Terminated"))
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                results.append((proc.info['name'], f"Failed: {str(e)}"))
        return results

    def start_services(self):
        results = []
        for service_name in self.target_services:
            try:
                win32serviceutil.StartService(service_name)
                results.append((service_name, "Started successfully"))
            except Exception as e:
                results.append((service_name, f"Failed: {str(e)}"))
        return results 