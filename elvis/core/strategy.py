from .q_values import QValues
from .eligibility_traces import EligibilityTraces


class Strategy:

    def __init__(self, gamma, alpha, _lambda, epsilon, epsilon_decay):
        """
        @param gamma discount-rate
        @param alpha learning rate
        @param _lambda decay-rate for eligibility traces
        @param epsilon for e-greedy exploration
        @param epsilon_decay epsilon decay factor
        """
        self.y = gamma
        self.a = alpha
        self.l = _lambda
        self.e = epsilon
        self.e_decay = epsilon_decay
        self.eligibility_traces = None
        self.q_values = QValues()
        self.episode = 0
        self.episode_reward = 0

    def new_episode(self):
        """
        Start a new episode. This increments the episode counter and decays
        the eligibility traces and epsilon values
        :return:
        """
        self.eligibility_traces = EligibilityTraces(1 - self.y * self.l)
        self.e *= self.e_decay
        self.episode += 1
        self.episode_reward = 0

    def next_action(self, state, e=None):
        """
        Choose the next action based on the e parameter or the e value the Strategy
        was initialized with
        :param state: the current actor state
        :param e: the e-greedy value, default is None
        :return: the next action
        """
        return self.q_values.get_greedy_action(state, self.e if e is None else e)

    def update(self, state_before, action, reward, state_after):
        """
        Updates the expected value for the given state, action pairs
        :param state_before: the current state of the actor
        :param action: the action to take
        :param reward: the actual reward for the action
        :param state_after: the state of the actor after the action
        :return: the TD Error
        """
        expected_reward = self.q_values.get_expected_reward(state_before, action)
        next_action = self.q_values.get_greedy_action(state_after, self.e)
        next_expected_reward = self.q_values.get_expected_reward(state_after, next_action)

        td_error = reward - expected_reward + self.y * next_expected_reward

        self.eligibility_traces.increment(state_before, action)
        self.q_values.ensure_exists(state_before, action)

        def update_q_values(state, act):
            old_expected_reward = self.q_values.get_expected_reward(state, act)
            new_expected_reward = old_expected_reward + self.a * td_error * self.eligibility_traces.get(state, act)
            self.q_values.set_expected_reward(state, act, new_expected_reward)
            self.eligibility_traces.decay(state, act)

        self.q_values.for_each(update_q_values)
        self.episode_reward += reward

        return td_error

    def snapshot(self):
        """
        Get a snapshot of the Strategy
        :return: a dict containing the current Q Values, the epsilon value
            and the current episode number
        """
        return {
            'q': self.q_values.get_all_values(),
            'ε': self.e,
            'episode': self.episode
        }