

class Strategy:

    def __init__(self, y, a, l, e, e_decay, actions):
        self.y = y
        self.a = a
        self.l = l
        self.e = e
        self.e_decay = e_decay
        self.actions = actions
        self.eligibility_traces = None
        self.q_values = QValues(actions)
        self.scores = [] # TODO
        self.episode = 0
        self.episode_reward = 0
        self.episode_reward_total = 0 # TODO

    def new_episode(self):
        self.eligibility_traces = EligibilityTraces(1 - self.y * self.l)
        self.e *= self.e_decay
        self.episode += 1
        self.episode_reward = 0

    def next_action(self, state, e=None):
        return self.q_values.get_greedy_action(state, self.e if e is None else e)

    def update(self, state_before, action, reward, state_after):
        expected_reward = self.q_values.get_expected_reward(state_before, action)
        next_action = self.q_values.get_greedy_action(state_after, self.e)
        next_expected_reward = self.q_values.get_expected_reward(state_after, next_action)

        td_error = reward - expected_reward + self.y * next_expected_reward

        self.eligibility_traces.increment(state_before, action)
        self.q_values.ensure_exists(state_before, action)

        def update_q_values(state, action):
            old_expected_reward = self.q_values.get_expected_reward(state, action)
            new_expected_reward = old_expected_reward + self.a * td_error * self.eligibility_traces.get(state, action)
            self.q_values.set_expected_reward(state, action, new_expected_reward)
            self.eligibility_traces.decay(state, action)

        self.q_values.for_each(update_q_values)
        self.episode_reward += reward

    def load(self, values):
        self.q_values.set_all_values(values['q'])
        self.e = values['e']
        self.scores = values['scores']
        self.episode = values['episode']
