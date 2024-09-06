import os
import sys
from cookiecutter.main import cookiecutter


def main():
    # Get the directory of the current script
    template_dir = os.path.dirname(os.path.abspath(__file__))

    # Parse command line arguments
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = os.getcwd()

    # Run cookiecutter
    cookiecutter(template_dir + "/", output_dir=output_dir, overwrite_if_exists=True)

    print(f"Django project created in {output_dir}")


if __name__ == "__main__":
    main()
