"""This is a hacky way to locally get the SimulinkCoSimulation submodule
into a state that works without creating our copy of it.

Run this script from the present directory
"""

import glob
import os
import shutil

COSIM = 'SimulinkCoSimulationExample'

print('Copying main gitignore file to Simulink example')
sub_ignore = f'./{COSIM}/.gitignore'
shutil.copy('../.gitignore', sub_ignore)

print('Ignoring ZeroMQ repositories and built executables in Simulink example git')
with open(sub_ignore, 'a') as sub_ignore_file:
    sub_ignore_file.write('''
cppzmq/
libzmq/
*.exe
''')

print('Copying ZeroMQ repositories into Simulink example')
for repo in ['cppzmq', 'libzmq']:
    shutil.rmtree(f'./{COSIM}/{repo}')
    shutil.copytree(f'./{repo}', f'./{COSIM}/{repo}')

print('Creating output directory of old build script')
binary_dir = f'./{COSIM}/libzmq/bin/x64/Release/v140/dynamic'
os.makedirs(binary_dir, exist_ok=True)

print('Copying pre-built binaries for 64-bit Windows')
for filename in glob.glob('./bin/win64/*'):
    basename = os.path.basename(filename)
    shutil.copy(filename, os.path.join(binary_dir, basename))

print('Patching done')
