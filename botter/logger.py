from datetime import datetime
import os


class BaseLogger:
    def __init__(self, base_dir, filename='log', debug=False):
        assert isinstance(filename, str), "Filename must be a string instace."
        if not filename.endswith('.log'):
            filename = '{}.log'.format(filename)
        self.file = os.path.join(base_dir, filename)
        self.debug = debug

    def __call__(self, data=None, instance=None):
        if instance:
            class_ = instance.__class__.__name__
        else:
            class_ = 'NOCLASS'

        line = "[{datetime}] [{class_}] {instance} - {message}".format(
            class_=class_,
            datetime=datetime.now().strftime('%c'),
            instance=str(instance) if instance else '',
            message=str(data) if data else '',
        )
        self.append_to_file(line)

    def append_to_file(self, line):
        try:
            with open(self.file, 'a') as file:
                if self.debug:
                    print(line)
                file.write('\n' + line)
        except Exception:
            pass
