# Requirements
- python == 3.12

# Repository Structure
```
./
|── results/
|── src/
|   |── problems/
|   |   |── __init__.py
|   |   |── helper.py
|   |   |── dynamic_programming/
|   |   |   |── __init__.py
|   |   |   |── knapsack.py
|   |   |   |── one_d.py
|   |   |   |── registry.py
|   |   |   |── two_d.py
|   ├── agent.py
|   ├── base.py
|   ├── main.py
|── test/
|── README.md
|── requirements.txt
```

# Setup
Run these commands at root of the repository:
```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd ./src
cp .env.example .env
# Edit .env to set your OpenAI API key

# Run the main script
python main.py
```
