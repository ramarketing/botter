from datetime import datetime


class BaseLogger:
    def __init__(self, debug=False):
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
        self.prepare_line(line)

    def prepare_line(self, line):
        print(line)
