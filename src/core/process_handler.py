import psutil
import win32serviceutil
import win32service
import platform
import os

class ProcessHandler:
    def __init__(self):
        # Detect system architecture
        self.is_64bits = platform.machine().endswith('64')
        
        # Use years for generic version selection
        self.office_versions = ["2007", "2010", "2013", "2016"] 
        
        # Define DLL patterns per application
        self.dll_patterns = {
            "Word": "DSP_01_{}{}.dll",
            "Excel": "DSP_03_{}{}.dll"
        }
        
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

    def _get_add_in_dll_name(self, app_type, office_year):
        """Generates the DLL name based on app type, year, and architecture."""
        pattern = self.dll_patterns.get(app_type)
        if not pattern:
            raise ValueError(f"Unknown application type: {app_type}")
            
        arch_suffix = "64" if self.is_64bits else ""
        return pattern.format(office_year, arch_suffix)
    
    def toggle_add_in(self, app_type, folder_path, office_year, disable=True):
        """Toggles the specified Office add-in DLL on or off."""
        try:
            dll_name = self._get_add_in_dll_name(app_type, office_year)
            dll_path = os.path.join(folder_path, dll_name)
            # Append underscore before the extension
            base, ext = os.path.splitext(dll_path)
            disabled_dll_path = f"{base}_{ext}" 
            
            action = "disable" if disable else "enable"
            source_path = dll_path if disable else disabled_dll_path
            target_path = disabled_dll_path if disable else dll_path
            
            not_found_path = dll_path if disable else disabled_dll_path
            expected_state = "enabled" if disable else "disabled"

            if os.path.exists(source_path):
                os.rename(source_path, target_path)
                return True, f"Successfully {action}d {dll_name}"
            else:
                return False, f"Could not {action}. DLL not found in the expected {expected_state} state: {os.path.basename(not_found_path)}"
                    
        except Exception as e:
            return False, f"Error during {action}: {str(e)}" 