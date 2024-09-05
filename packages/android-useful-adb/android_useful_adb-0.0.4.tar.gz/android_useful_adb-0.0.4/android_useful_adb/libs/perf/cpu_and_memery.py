
from datetime import datetime
import subprocess
import time


class Top:
    def __init__(self,process:subprocess.Popen):
        self.p = process
        self.total = []
    def get_data(self,pid ,duration =None):
        try:
            if duration is not None:
                start_time = datetime.now().timestamp()
            
            while True:
                if duration is not None and datetime.now().timestamp() - start_time > duration:
                    break
                # 读取一行输出
                self.dispose_data(pid)
        except KeyboardInterrupt:
            # 如果需要处理用户中断（例如使用 Ctrl+C），可以在这里添加代码
            print("Process was terminated by user.")
        finally:
            # 确保进程被正确终止
            self.p.terminate()
            self.p.wait()
        return self.total
    
    def dispose_data(self,pid):
        line = self.p.stdout.readline().decode("utf-8")
        if str(pid) in str(line):
            ret = line.split()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            self.total.append({'time':current_time,'RES':ret[1],'SHR':ret[2],'%CPU':ret[3],'%MEM':ret[4]})


class Cpu:
    def __init__(self,total_cpu,process_cpu,interval=1):
        self.total_cpu = total_cpu
        self.process_cpu = process_cpu
        self.interval = interval # 数据获取间隔

    '''
    计算某进程的cpu使用率
    100*( processCpuTime2 – processCpuTime1) / (totalCpuTime2 – totalCpuTime1) (按100%计算，如果是多核情况下还需乘以cpu的个数);
    cpukel cpu几核
    pid 进程id
    '''
    def cpu_rate(self):
        
        process_cputime_begain = self.process_cpu()
        time.sleep(self.interval)
        process_cputime2_end = self.process_cpu()

        total_cputime_begain = self.total_cpu()
        time.sleep(self.interval)
        total_cputime_end = self.total_cpu()
        

        # 按总量100%算原本应该除以cpu核数，现在是按100%*cpu核数
        cpu = 100 * (process_cputime2_end-process_cputime_begain) / (total_cputime_end - total_cputime_begain)
        # cpu = 100 * process_cputime_begain/total_cputime_begain
        cpu = round(cpu, 2)
        return cpu
