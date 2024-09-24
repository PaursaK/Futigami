class Logger:
    '''Singleton Design Pattern employed for logger'''
    _instance = None
    
    def __new__(cls, log_file="data_log.txt"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.log_file = log_file
            # Open the log file in append mode
            with open(cls._instance.log_file, "a", encoding="utf-8") as file:
                file.write("Starting new log session\n")
        return cls._instance
    
    def log(self, message):
        """Write a message to the log file."""
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(message + "\n")
