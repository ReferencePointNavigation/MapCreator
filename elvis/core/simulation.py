import sys


class Simulation:
    """
    The Simulation class encapsulates a full series of Episodes
    """
    def __init__(self, config, actor, strategy, environment):
        self.config = config
        self.actor = actor
        self.strategy = strategy
        self.environment = environment
        self.optimal = (sys.maxsize, -sys.maxsize, {})

    def run(self):
        for episode_index in range(self.config['episode-count']):
            steps, reward = self.run_episode()
            if steps < self.optimal[0] and reward > self.optimal[1]:
                self.optimal = (steps, reward, self.strategy.snapshot())
        print(self.optimal)

    def run_episode(self):
        """
        A single episode of the Simulation
        :return: the total number of steps to reach the goal,
            the total rewards for the episode
        """
        steps = 0
        total_reward = 0

        self.strategy.new_episode()

        while not self.actor.in_terminal_state() and steps < self.config['episode-steps']:
            state_before = self.actor.get_position()
            action = self.strategy.next_action(state_before)
            reward = self.environment.perform_action(action)
            state_after = self.actor.get_position()
            self.strategy.update(state_before, action, reward, state_after)
            total_reward = total_reward + reward
            steps = steps + 1

        self.environment.reset()

        return steps, total_reward

    def get_results(self):
        """
        Get the results of the simulation
        :return: a Tuple (min(steps), max(reward), strategy)
        """
        return self.optimal