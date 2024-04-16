from glob import glob
from pprint import pprint

from jinja2 import Environment, FileSystemLoader
evaluators_files = glob("evaluators_prompts/*.jinja2")
evaluators = {}
for evaluator_file in evaluators_files:
    print(evaluator_file)
    with open(evaluator_file) as f:
        evaluators[evaluator_file] = f.read()

pprint(evaluators)

# change vars in jinja2 template
question = "What is the first letter of the alphabet?"
answer = "a"

for evaluator_file, evaluator in evaluators.items():
    print(evaluator_file)
    template = Environment(loader=FileSystemLoader('.')).from_string(evaluator)
    print(template.render(question=question, answer=answer))
    print()