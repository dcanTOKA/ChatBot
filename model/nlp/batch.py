class Batch:
    def __init__(self, input_variable, input_length, target_variable, mask, max_target_len):
        self.input_variable= input_variable
        self.input_length= input_length
        self.target_variable = target_variable
        self.mask = mask
        self.max_target_len = max_target_len
