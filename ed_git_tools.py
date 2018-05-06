import subprocess

def run_command(path, command):
    with subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path) as process:
        return process.communicate()[0].decode('utf-8')

def status(path):
    return run_command(path, ['git', 'status'])

def fetch(path):
    return run_command(path, ['git', 'fetch', '--all'])
