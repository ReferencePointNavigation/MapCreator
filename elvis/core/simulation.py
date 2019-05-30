MAX_EPISODE_STEPS = 100000


class Simulation:

    def __init__(self, config, actor, strategy, environment):
        self.episode_count = config['episode-count']
        self.save_interval = config['save-interval']
        self.actor = actor
        self.strategy = strategy
        self.environment = environment

    def run(self):
        for episode_index in range(self.episode_count):
            self.run_episode()
            if episode_index > 0 and episode_index % self.save_interval == 0:
                self.save_to_file(self.strategy)
                print(episode_index)

    def run_episode(self):
        steps = 0
        total_reward = 0

        self.strategy.new_episode()

        while not self.environment.actor_in_terminal_state() and steps < MAX_EPISODE_STEPS:
            state_before = self.environment.get_actor_state()
            action = self.strategy.next_action(state_before)
            reward = self.environment.perform_action(action)
            state_after = self.environment.get_actor_state()
            self.strategy.update(state_before, action, reward, state_after)
            total_reward += reward
            steps += 1

        return steps, total_reward

    def save_to_file(self, strategy):
        pass