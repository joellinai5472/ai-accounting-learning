from pathlib import Path
import runpy
root=Path.cwd()
(root/'.cache-build').mkdir(exist_ok=True)
(root/'_site').mkdir(exist_ok=True)
for module in ['prepare.py','render.py','package.py','split_online.py','validate.py']:
    runpy.run_path(str(root/'src'/module),run_name='__main__')
