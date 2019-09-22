import os
import subprocess

print("Example 1:")
os.system("vcgencmd measure_temp")

print("\nExample 2:")
shell_stdout = os.popen('vcgencmd measure_temp').read()
print(shell_stdout)

print("Example 3:")
shell_process = subprocess.Popen(['vcgencmd', 'measure_temp'],  # command as string array
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
stdout, stderr = shell_process.communicate()               # run shell process, returns 2 byte arrays
print("Returncode: {}".format(shell_process.returncode))   # return code of shell process
print("Standard Out: {}".format(stdout.strip().decode()))  # stdout contains byte array with newline
                                                           #  strip removes newline, decoding byte array results into string
print("Standard Error: {}".format(stderr))                 # stderr is empty byte array, since this process succeeded

print("\nExample 4:")
shell_process = subprocess.Popen(['ls', 'invalid_path'],  # command as string array
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
stdout, stderr = shell_process.communicate()                 # run shell process, returns 2 byte arrays
print("Returncode: {}".format(shell_process.returncode))     # return code of shell process
print("Standard Out: {}".format(stdout))                     # stdout is empty byte array, since this process failed
print("Standard Error: {}".format(stderr.strip().decode()))  # stderr contains byte array with newline
                                                             #  strip removes newline, decoding byte array results into string

print("\nExample 5:")
shell_process = subprocess.Popen("ls invalid_path",   # command as string since shell is true
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)  # stderr will be piped into stdout
stdout = shell_process.communicate()[0]                     # first element, since stdout contains both, stdout and stderr
                                                            # stderr is empty byte array, since stderr is piped into stdout
print("Returncode: {}".format(shell_process.returncode))    # return code of shell process
print("Standard Out: {}".format(stdout.strip().decode()))   # stdout contains byte array with newline
                                                            #  strip removes newline, decoding byte array results into string
