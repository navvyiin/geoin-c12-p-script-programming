install:
	python -m pip install -e .

test:
	pytest

demo:
	python examples/demo_workflow.py

clean:
	python -c "import shutil; from pathlib import Path; [shutil.rmtree(p, ignore_errors=True) for p in ['outputs','logs']]"
