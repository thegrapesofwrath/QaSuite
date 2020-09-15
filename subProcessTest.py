#%%
import subprocess
#%%

testFile = "./bugList_09022020_JeremyDavid.txt"

#%%
linter_commands = ["cspell", "-u", testFile]
completed = subprocess.run(
            linter_commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
# %%
print(completed.stdout)
# %%
type(completed.stdout)
# %%
stdOut = str(completed.stdout)
#%%
stdOut = stdOut.split('\\n')
stdOut[0] = stdOut[0][1:]
stdOut = stdOut[1:len(stdOut) - 1]
# %%
# stdOut = list(stdOut.split('\n'))
stdOut = stdOut.split('\\n')
# %%
stdOut.splitlines()
# %%
stdOut.split('\\n')
# %%
