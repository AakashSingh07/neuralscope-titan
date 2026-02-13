FROM python:3.11-slim

WORKDIR /app

COPY ../goal_analysis/goal_parser.py ./goal_parser.py
COPY ../agent_architecture/architecture_selector.py ./architecture_selector.py
COPY ../code_generator/codegen.py ./codegen.py

RUN pip install transformers torch

CMD ["python3", "goal_parser.py"]
