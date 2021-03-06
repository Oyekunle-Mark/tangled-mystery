import random

from util import Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        # iterate over 0 to num users...
        for i in range(0, num_users):
            # add user using an f-string
            self.add_user(f"User {i}")

        # Create friendships
        # generate all possible friendship combinations
        possible_friendships = []

        # avoid duplicates by making sure the first number is smaller than the second
        # iterate over user id in users...
        for user_id in self.users:
            # iterate over friend id in in a range from user id + 1 to last id + 1...
            for friend_id in range(user_id + 1, self.last_id + 1):
                # append a user id and friend id tuple to the possible friendships
                possible_friendships.append((user_id, friend_id))

        # shuffle friendships random import
        random.shuffle(possible_friendships)

        # create friendships for the first N pairs of the list
        # N is determined by the formula: num users * avg friendships // 2
        # NOTE: need to divide by 2 since each add_friendship() creates 2 friendships
        # iterate over a range using the formula as the end base...
        for i in range(num_users * avg_friendships // 2):
            # set friendship to possible friendships at i
            friendship = possible_friendships[i]
            # add friendship of frienship[0], friendship[1]
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # keep track of visited
        visited = {}  # Note that this is a dictionary, not a set
        # instantiate the queue class
        queue = Queue()
        # enqueue the starting user_id as a list
        queue.enqueue([user_id])

        # loop while queue is not empty
        while queue.size():
            # dequeue a path from the queue
            path = queue.dequeue()
            # grab the last user_id from the path
            current_user_id = path[-1]

            # if current_user_id has not been visited
            if current_user_id not in visited:
                # add it to visited as current_user_id as key and path as value
                visited[current_user_id] = path

                # for every friendships of the current_user_id
                for id in self.friendships[current_user_id]:
                    # create a copy of path
                    new_path = list(path)
                    # append id to the new path
                    new_path.append(id)
                    # enqueue the newly generated path
                    queue.enqueue(new_path)

        # return visited
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
