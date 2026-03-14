import subprocess, os

os.chdir('.')  # run from same dir as chal_patched

# Read g_vault_byte (created on first run of original chal)
with open('.vault_state', 'rb') as f:
    vault_byte = f.read(1)[0]

argv0 = './chal_patched'
argv0_len = len(argv0) & 0xFF

proc = subprocess.Popen([argv0], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
pid = proc.pid
pid_seed = (pid ^ (pid >> 8)) & 0xFF
key = (pid_seed ^ vault_byte) ^ argv0_len

print(f"PID={pid}, pid_seed={pid_seed:#x}, vault_byte={vault_byte:#x}, key={key:#x}")
stdout, _ = proc.communicate(input=b'anyoperator\n' + f'{key:x}\n'.encode())
print(stdout.decode())
