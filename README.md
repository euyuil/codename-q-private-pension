# Private pension

## Deploy

Initial deployment:

```bash
python3 -m venv venv
source venv/bin/activate

pip config -v list
vim /home/ecs-user/.pip/pip.conf
```

Add this:

```ini
[global]
timeout = 60
index-url = https://pypi.doubanio.com/simple
```

Then:

```bash
pip install -r requirements.txt
```
