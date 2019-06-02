MAX_EPISODE_STEPS = 1000


class Simulation:

    def __init__(self, config, actor, strategy, environment):
        self.config = config
        self.actor = actor
        self.strategy = strategy
        self.environment = environment

    def run(self):
        for episode_index in range(self.config['episode-count']):
            steps, reward = self.run_episode()
            if episode_index > 0 and episode_index % self.config['save-interval'] == 0:
                self.save_to_file(self.strategy)
                #print('{0}:{1} = {2}'.format(episode_index, steps, reward))

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
            total_reward = total_reward + reward
            steps = steps + 1

        self.environment.reset()

        print('{0}:{1}'.format(str(steps), str(total_reward)))

        return steps, total_reward

    def save_to_file(self, strategy):
        print(strategy.dump())