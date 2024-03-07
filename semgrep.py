import subprocess
import os
import tempfile


def run_semgrep(rule_file, target_dir):
    """
        Function to execute the semgrep scan
    """
    semgrep_cmd = f"semgrep -f {rule_file} {target_dir}"
    try:
        result = subprocess.run(semgrep_cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Semgrep failed with error: {e}")
        return ""

def prepend_errors_to_file(errors, target_file):
    """
        Temporary dile to prepend errors
    """
    with open(target_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(errors)
        f.write('\n\n')
        f.write(content)

def main():
    rules_directory = "semgrep_rules"

    target_directory = "src"

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
        tmp_file_name = tmp_file.name

        """
            Here we Iterate through rule files in the rules directory --> semgrep_rules
        """
        for rule_file in os.listdir(rules_directory):
            if rule_file.endswith(".yaml"):
                rule_path = os.path.join(rules_directory, rule_file)
                errors = run_semgrep(rule_path, target_directory)
                if errors:
                    tmp_file.write(errors)

        """
            Here we Prepend errors to target files
        """
        with open(tmp_file_name, 'r') as tmp_file:
            all_errors = tmp_file.read()
            for root, dirs, files in os.walk(target_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    prepend_errors_to_file(all_errors, file_path)

        """
            Function to remove the remporary file
        """
        os.remove(tmp_file_name)

if __name__ == "__main__":
    main()
