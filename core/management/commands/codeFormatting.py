import subprocess

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Format code with 4 spaces, sort imports, remove extra line spaces, and remove unused imports for Python, JavaScript, HTML, and CSS files.'

    def add_arguments(self, parser):
        parser.add_argument(
            'files', nargs='+', type=str, help='Files to format'
        )

    def handle(self, *args, **kwargs):
        files = kwargs['files']

        for file_path in files:
            self.format_code(file_path)

    def format_code(self, file_path):
        try:
            if file_path.endswith('.py'):
                # Step 1: Remove unused imports using autoflake
                subprocess.run(
                    [
                        'autoflake',
                        '--in-place',
                        '--remove-all-unused-imports',
                        '--remove-unused-variables',
                        file_path,
                    ],
                    check=True,
                )

                # Step 2: Format code with 4 spaces for indentation using black
                subprocess.run(
                    [
                        'black',
                        file_path,
                        '--line-length',
                        '79',
                        '--skip-string-normalization',
                    ],
                    check=True,
                )

                # Step 3: Sort imports using isort
                subprocess.run(['isort', file_path], check=True)

                # Step 4: Remove extra line spaces manually
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                formatted_lines = []
                for line in lines:
                    if line.strip() == "":
                        if (
                            len(formatted_lines) > 0
                            and formatted_lines[-1].strip() == ""
                        ):
                            continue
                    formatted_lines.append(line)

                with open(file_path, 'w') as file:
                    file.writelines(formatted_lines)

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully formatted {file_path}')
                )
            elif file_path.endswith(('.js', '.html', '.css')):
                # Format JavaScript, HTML, and CSS files using prettier
                subprocess.run(
                    ['npx', 'prettier', '--write', file_path], check=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully formatted {file_path}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipped {file_path}: Unsupported file type'
                    )
                )

        except subprocess.CalledProcessError as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to format {file_path}: {e}')
            )
