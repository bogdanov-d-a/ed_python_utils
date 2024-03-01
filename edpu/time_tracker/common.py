from edpu import calc_time_utils as CTU

def fail(msg='fail'):
    raise Exception(msg)

def key_sorted_dict_items(dict_):
    return sorted(dict_.items(), key=lambda t: t[0])

def add_int_to_dict(dict_, key, incr):
    if key not in dict_:
        dict_[key] = 0
    dict_[key] += incr
    if dict_[key] == 0:
        del dict_[key]

def sub_int_from_dict(dict_, key, decr):
    add_int_to_dict(dict_, key, -decr)

def dict_to_text(title, dict_):
    str_ = title + ':\n'
    for name, time in key_sorted_dict_items(dict_):
        if time == 0:
            fail()
        str_ += name + ' - ' + CTU.duration_string_with_negative(time) + '\n'
    return str_

class ReportBuilder:
    def __init__(self):
        self.checked_in = {}
        self.checked_out = {}

    def checkin(self, label, time):
        if type(label) is not str:
            fail()
        if type(time) is str:
            time = CTU.parse_duration(time)

        add_int_to_dict(self.checked_in, label, time)

    def remove(self, label, time):
        if type(label) is not str:
            fail()
        if type(time) is str:
            time = CTU.parse_duration(time)

        sub_int_from_dict(self.checked_in, label, time)

    def rename(self, label, new_label):
        if type(label) is not str:
            fail()
        if type(new_label) is not str:
            fail()

        time = self.checked_in[label]
        sub_int_from_dict(self.checked_in, label, time)
        add_int_to_dict(self.checked_in, new_label, time)

    def transfer_time(self, src_label, dst_label, time):
        self.remove(src_label, time)
        self.checkin(dst_label, time)

    def checkout(self, label, time):
        if type(label) is not str:
            fail()
        if type(time) is str:
            time = CTU.parse_duration(time)

        sub_int_from_dict(self.checked_in, label, time)
        add_int_to_dict(self.checked_out, label, time)

    def checkout_one(self, label):
        self.checkout(label, self.checked_in[label])

    def checkout_all(self):
        for label, time in key_sorted_dict_items(self.checked_in):
            self.checkout(label, time)

    def pending_time(self):
        result = 0
        for _, time in key_sorted_dict_items(self.checked_in):
            result += time
        return result

    def checked_out_time(self):
        result = 0
        for _, time in key_sorted_dict_items(self.checked_out):
            result += time
        return result

    def total_time(self):
        return self.pending_time() + self.checked_out_time()

    def get_warnings(self):
        return []

    def get_summary(self):
        result = ''

        if len(self.checked_in) > 0:
            result += dict_to_text('Pending tasks', self.checked_in) + '\n'

        if len(self.checked_out) > 0:
            result += dict_to_text('Checked out tasks', self.checked_out) + '\n'

        result += 'Checked out: ' + CTU.duration_string_with_negative(self.checked_out_time()) + '\n'
        result += 'Pending time: ' + CTU.duration_string_with_negative(self.pending_time()) + '\n'
        result += 'Total time: ' + CTU.duration_string_with_negative(self.total_time()) + '\n'

        return result

class ReportBuilder2(ReportBuilder):
    def __init__(self):
        ReportBuilder.__init__(self)
        self.ongoing_action = None
        self.allowed_leaps = 0

    def start(self, label, time):
        if type(time) is str:
            time = CTU.parse_time_point(time)
        if self.ongoing_action is not None:
            fail(self.ongoing_action[0] + ' already running, can\'t start ' + label + ' at ' + CTU.time_point_string(time))
        self.ongoing_action = (label, time)

    def stop(self, time):
        if type(time) is str:
            time = CTU.parse_time_point(time)
        if self.ongoing_action is None:
            fail('Nothing to stop (at ' + CTU.time_point_string(time) + ')')

        label = self.ongoing_action[0]
        passed_time = time - self.ongoing_action[1]
        if passed_time < 0:
            if self.allowed_leaps <= 0:
                fail('Not enough dayleaps for period ' + CTU.time_point_string(self.ongoing_action[1]) + ' - ' + CTU.time_point_string(time))
            self.allowed_leaps -= 1
            passed_time += 24 * 60

        self.checkin(label, passed_time)
        self.ongoing_action = None

    def switch(self, label, time):
        if type(time) is str:
            time = CTU.parse_time_point(time)
        self.stop(time)
        self.start(label, time)

    def allow_leap(self):
        self.allowed_leaps += 1

    def remove_ongoing(self, time):
        if type(time) is str:
            time = CTU.parse_duration(time)
        if self.ongoing_action is None:
            fail('No ongoing task to get ' + CTU.duration_string_with_negative(time) + ' from')

        self.remove(self.ongoing_action[0], time)

    def transfer_time_ongoing(self, dst_label, time):
        if self.ongoing_action is None:
            fail('No ongoing task to get ' + CTU.duration_string_with_negative(time) + ' from')

        self.transfer_time(self.ongoing_action[0], dst_label, time)

    def touch(self, time):
        if type(time) is str:
            time = CTU.parse_time_point(time)
        if self.ongoing_action is None:
            fail('No ongoing task to touch at ' + CTU.time_point_string(time))

        self.switch(self.ongoing_action[0], time)

    def get_warnings(self):
        result = ReportBuilder.get_warnings(self)
        if self.ongoing_action is not None:
            result.append('Active task (since '
                          + CTU.time_point_string(self.ongoing_action[1])
                          + '): ' + self.ongoing_action[0])
        if self.allowed_leaps != 0:
            result.append(str(self.allowed_leaps) + ' day leaps are not used')
        return result

class ReportBuilder3(ReportBuilder2):
    def __init__(self):
        ReportBuilder2.__init__(self)
        self.task_stack = []

    def push(self, label, time):
        if type(time) is str:
            time = CTU.parse_time_point(time)
        self.task_stack.append(self.ongoing_action[0])
        self.switch(label, time)

    def push_stop(self, time):
        if type(time) is str:
            time = CTU.parse_time_point(time)
        self.task_stack.append(self.ongoing_action[0])
        self.stop(time)

    def pop(self, time):
        if type(time) is str:
            time = CTU.parse_time_point(time)
        self.switch(self.task_stack.pop(), time)

    def pop_stop(self, time):
        if type(time) is str:
            time = CTU.parse_time_point(time)
        self.start(self.task_stack.pop(), time)

    def drop_stack(self):
        self.task_stack = []

    def get_warnings(self):
        result = ReportBuilder2.get_warnings(self)
        if len(self.task_stack) != 0:
            result.append('Task stack is not empty: ' + ', '.join(self.task_stack))
        return result

ACTION_TYPES = [
    'start',
    'stop',
    'switch',
    'push',
    'push-stop',
    'pop',
    'pop-stop',
    'checkin',
    'checkout',
    'checkout-one',
    'checkout-all',
    'dayleap',
    'remove',
    'remove-ongoing',
    'transfer-time',
    'transfer-time-ongoing',
    'touch',
    'rename',
    'drop-stack',
]

class ActionType:
    def __init__(self, action):
        self._id = ACTION_TYPES.index(action)

    def equals(self, other):
        return self._id == other._id if type(other) is ActionType else self.equals(ActionType(other))

    def to_string(self):
        return ACTION_TYPES[self._id]

def apply_action(builder, action):
    type_ = ActionType(action[0])
    if type_.equals('start'):
        builder.start(action[1], action[2])
    elif type_.equals('stop'):
        builder.stop(action[1])
    elif type_.equals('switch'):
        builder.switch(action[1], action[2])
    elif type_.equals('push'):
        builder.push(action[1], action[2])
    elif type_.equals('push-stop'):
        builder.push_stop(action[1])
    elif type_.equals('pop'):
        builder.pop(action[1])
    elif type_.equals('pop-stop'):
        builder.pop_stop(action[1])
    elif type_.equals('checkin'):
        builder.checkin(action[1], action[2])
    elif type_.equals('checkout'):
        builder.checkout(action[1], action[2])
    elif type_.equals('checkout-one'):
        builder.checkout_one(action[1])
    elif type_.equals('checkout-all'):
        builder.checkout_all()
    elif type_.equals('dayleap'):
        builder.allow_leap()
    elif type_.equals('remove'):
        builder.remove(action[1], action[2])
    elif type_.equals('remove-ongoing'):
        builder.remove_ongoing(action[1])
    elif type_.equals('transfer-time'):
        builder.transfer_time(action[1], action[2], action[3])
    elif type_.equals('transfer-time-ongoing'):
        builder.transfer_time_ongoing(action[1], action[2])
    elif type_.equals('touch'):
        builder.touch(action[1])
    elif type_.equals('rename'):
        builder.rename(action[1], action[2])
    elif type_.equals('drop-stack'):
        builder.drop_stack()
    else:
        fail()
