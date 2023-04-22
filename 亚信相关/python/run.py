import subprocess
import time

if __name__ == '__main__':
    programs = ['Ntrtscan.exe', 'PccNT.exe', 'PccNTMon.exe']
    for program in programs:
        process = subprocess.Popen(f'start /B {program}', shell=True)
        time.sleep(1)
    input("如果OA安全检查已经通过，就按回车键继续...")
    for program in programs:
        subprocess.Popen(f'taskkill /f /im {program}')