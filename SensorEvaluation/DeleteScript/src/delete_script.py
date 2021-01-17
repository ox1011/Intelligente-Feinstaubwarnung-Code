import subprocess
import logging
import update_script

MAX_WORKLOAD_IN_PERCENT = 80

if __name__ == "__main__":
    # logging setting
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.getLogger('pika').setLevel(logging.WARNING)
    log = logging.getLogger()

    # get terminal output from df -h (disk space usage)
    proc = subprocess.Popen("df -h", shell=True, stdout=subprocess.PIPE, )
    output = str(proc.communicate()[0])

    hdd = "/dev/sda2"
    index_start = output.index(hdd)
    l = [i for i in range(len(output)) if output.startswith("%", i)]
    l.sort()

    index_end = 0
    for elem in l:
        if elem > index_start:
            index_end = elem
            break

    current_workload_in_percent = int(output[index_start:index_end].split(" ")[-1])

    if (current_workload_in_percent > MAX_WORKLOAD_IN_PERCENT) and update_script.check_right_password_DB(log):
        log.info("Start delete process")
        update_script.delete_data_DB(update_script.SQL_STMT_DELETE_SENSORDATAVALUES_OLDEST_DAY)
        log.info("Finish delete process")
    else:
        log.error("Delete process failed")
