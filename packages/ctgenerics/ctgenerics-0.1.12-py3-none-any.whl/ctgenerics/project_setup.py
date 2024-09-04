import os

class ProjectSetup:
    def __init__(self) -> None:
    
        self.project_name = input('Enter the name of the project: ')
        self.project_description = input('Enter a description for the project: ')
        self.author = input('Enter the author of the project: ')
        
        self.setup_project()

    def setup_project(self):
        if self.is_project_setup():
            self.create_file_structure()
            self.create_gitignore()
            self.populate_readme()
            


    def is_project_setup(self):
        if os.path.exists('setup.cfg'):
            print('you have already setup a project in this directory')
            return False
        else:
            
            return True
    def create_gitignore(self):
        with open(f'{self.project_name}/.gitignore', 'w') as f:
            f.write('*.pyc\n__pycache__\n')
        print('.gitignore created.')

    def populate_readme(self):
        with open(f'{self.project_name}/README.md', 'w') as f:
            f.write(f'## {self.project_name}\n\n{self.project_description}\n\n### Author\n{self.author}')
        print('README.md created.')

    def create_file_structure(self):
        if os.path.isdir(self.project_name):
            print('Project directory already exists.')
            return
        os.makedirs(os.path.join(self.project_name, 'src'))
        os.makedirs(os.path.join(self.project_name, 'tests'))
        os.makedirs(os.path.join(self.project_name, 'data'))
        os.makedirs(os.path.join(self.project_name, '.ctgenerics_cache'))

        # Create __init__.py files
        open(os.path.join(self.project_name, 'src', '__init__.py'), 'a').close()
        open(os.path.join(self.project_name, 'src', 'main.py'), 'a').close()
        open(os.path.join(self.project_name, 'tests', '__init__.py'), 'a').close()
        # Create setup.cfg in the cache directory
        with open(os.path.join(self.project_name, '.ctgenerics_cache', 'setup.cfg'), 'w') as f:
            f.write(f'[metadata]\nname = {self.project_name}\nauthor = {self.author}\n')
            print('File structure created.')

def main():
    ProjectSetup()
if __name__ == '__main__':
    main()