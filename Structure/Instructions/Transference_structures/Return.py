class Return:
    def __init__(self, val, ret_type, is_temp, aux_type=""):
        self.value = val
        self.type = ret_type
        self.aux_type = aux_type
        self.is_temp = is_temp
        self.true_lbl = ''
        self.false_lbl = ''
