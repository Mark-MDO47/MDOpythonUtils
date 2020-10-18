# mdoAnsibleLint

mdoAnsibleLint - start of a simple "lint" for Ansible YAML files
- inspiration came from spending all day looking for a missing ":"
  - ansible-playbook, ansible-lint and yamllint were not leading me to the culprit
- example: `python mdoAnsibleLint.py test.yml`
- example: for v in \`find ansible_mdo -name "*.yml"\`; do python mdoAnsibleLint.py $v; done
- -v, --verbose  always display contents of parsed YAML
- at this time, just does yaml.load() then looks for missing ":" at first level

`$ python mdoAnsibleLint.py -h`
- usage: mdoAnsibleLint oneYamlFile.yml
- stdout receives warnings/errors found in *.yml file
- positional arguments:
  - yamlFile       path to a single YAML file
- optional arguments:
  - -h, --help     show this help message and exit
  - -v, --verbose  always display contents of parsed YAML
- Example:
- python mdoAnsibleLint.py test.yml

NOTE: -h also gives an example "for" loop that I just cannot get to format correctly in markdown; do the command to see it
