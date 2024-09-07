import subprocess
import os
import tempfile
import time

def test_supervisor_tee():
    # Create a temporary directory for Supervisor logs
    with tempfile.TemporaryDirectory() as tempdir:
        stdout_log = os.path.join(tempdir, 'vnc-stdout.log')
        stderr_log = os.path.join(tempdir, 'vnc-stderr.log')

        # Create a Supervisor configuration file
        supervisor_conf = f"""
        [supervisord]
        logfile={tempdir}/supervisord.log
        pidfile={tempdir}/supervisord.pid

        [program:vnc]
        command=python3 {os.path.abspath('supervisor_tee.py')}
        stdout_logfile={stdout_log}
        stderr_logfile={stderr_log}
        stdout_logfile_maxbytes=50MB
        stderr_logfile_maxbytes=50MB
        stdout_logfile_backups=5
        stderr_logfile_backups=5
        stdout_capture_maxbytes=50MB
        stderr_capture_maxbytes=50MB
        """

        conf_path = os.path.join(tempdir, 'supervisord.conf')
        with open(conf_path, 'w') as f:
            f.write(supervisor_conf)

        # Start Supervisor
        subprocess.run(['supervisord', '-c', conf_path])

        # Give Supervisor some time to start
        time.sleep(5)

        # Check if the log files are created
        assert os.path.exists(stdout_log)
        assert os.path.exists(stderr_log)

        # Stop Supervisor
        subprocess.run(['supervisorctl', '-c', conf_path, 'shutdown'])
