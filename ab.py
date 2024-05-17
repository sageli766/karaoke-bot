import os
from subprocess import Popen, PIPE, CalledProcessError

# Path to the directory containing the executable
working_directory = "C:\\Program Files\\DAIICHIKOSHO Karaoke@DAM"

# Path to the executable
exe_path = os.path.join(working_directory, "DKKaraokeWindows.exe")

# Ensure the path is quoted correctly
quoted_exe_path = f'"{exe_path}"'

try:
    with Popen(quoted_exe_path, stdout=PIPE, bufsize=1, universal_newlines=True, cwd=working_directory, shell=True) as p:
        print(p)  # Print the Popen object

        # Print stdout continuously
        for stdout_line in iter(p.stdout.readline, ''):
            print(stdout_line, end='')

        # Print stderr continuously
        for stderr_line in iter(p.stderr.readline, ''):
            print(stderr_line, end='')

        # Wait for the process to complete and get the return code
        return_code = p.wait()

    # Print the return code
    print(f"\nProcess return code: {return_code}")

    if return_code != 0:
        raise CalledProcessError(return_code, p.args)
except FileNotFoundError:
    print(f"The file {exe_path} does not exist.")
except CalledProcessError as e:
    print(f"Process failed with return code {e.returncode}")