import os
from subprocess import run

run(["python", 'LimitingSeaStates.py', '--nogui'])

# # List with folders that need to be run
#
# queue = [
#     'LC0S',
#     'LC5S\\0.02 m.s lowering',
#     'LC5S\\0.04 m.s lowering'
# ]
#
# currentWD = os.getcwd()
#
# for item in queue:
#
#     completed = False
#
#     os.chdir(os.path.join(currentWD, item))
#
#     while not completed:
#         run(["python", 'LimitingSeaStates.py', '--nogui'])
#
#         if os.path.isfile('completed.txt'):
#             completed = True
#         else:
#             completed = False


