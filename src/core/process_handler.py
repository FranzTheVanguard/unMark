import psutil
import win32serviceutil
import win32service
import platform
import os

class ProcessHandler:
    def __init__(self):
        # Detect system architecture
        self.is_64bits = platform.machine().endswith('64')
        
        # Initialize word_versions
        self.word_versions = ["Word 2007", "Word 2010", "Word 2013", "Word 2016"]
        
        # Filter processes based on architecture

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
        
        self.dll_pattern = "DSP_01_{}{}.dll"
    
    def get_architecture(self):
        return "64-bit" if self.is_64bits else "32-bit"

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

    def get_dll_name(self, word_version):
        # Extract year from version string (e.g., "Word 2013" -> "2013")
        year = word_version.split()[-1]
        arch_suffix = "64" if self.is_64bits else ""
        return self.dll_pattern.format(year, arch_suffix)
    
    def toggle_dll(self, folder_path, word_version, disable=True):
        try:
            dll_name = self.get_dll_name(word_version)
            dll_path = os.path.join(folder_path, dll_name)
            disabled_dll_path = f"{dll_path[:-4]}_.dll"
            
            if disable:
                # Check if original DLL exists
                if os.path.exists(dll_path):
                    os.rename(dll_path, disabled_dll_path)
                    return True, f"Successfully disabled {dll_name}"
                else:
                    return False, f"DLL {dll_name} not found"
            else:
                # Check if disabled DLL exists
                if os.path.exists(disabled_dll_path):
                    os.rename(disabled_dll_path, dll_path)
                    return True, f"Successfully enabled {dll_name}"
                else:
                    return False, f"Disabled DLL {dll_name}_ not found"
                    
        except Exception as e:
            return False, f"Error: {str(e)}" 