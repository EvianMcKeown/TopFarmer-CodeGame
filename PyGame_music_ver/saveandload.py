# saveandload.py

class SaveAndLoad:
    def __init__(self):
        self.code_file = "code_save.txt"

    def save_code(self, code):
        try:
            file = open(self.code_file, 'w')
            file.write(code)
            file.close()
        except IOError:
            print("Error: Could not write file")

    def load_code(self):
        code = ""  # Initialize with a default value
        try:
            file = open(self.code_file, 'r')
            code = file.read()
            file.close()
        except IOError:
            print("Error: Could not read file")
        return code