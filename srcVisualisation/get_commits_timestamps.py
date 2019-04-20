import time
import numpy as np
import pandas as pd
from github import Github
from github import GithubException


def get_commits_timestamps(github_client, repository_name, max_commit_number = 200):
    '''
    Returns:
        - commit timestamps for the specified repository
        - lower bound of number of commits to be plotted
        - total number of commits for that repository(higher bound of number of commits to be plotted)
    max_commit_number: maximum number of entries that shall be returned(if the repository has fewer
                       commits than all the available ones will be returned)
    '''

    try:
        repo = github_client.get_repo(repository_name)

        commits           = repo.get_commits()
        number_of_commits = commits.totalCount

        # get the commit timestamps
        counter = 0
        commits_timestamps = []

        for commit in commits:
            if commit.commit is not None:
                commits_timestamps.append(commit.commit.author.date)
                counter += 1

                if counter == max_commit_number:
                    break

        # the commits are given from newer to older so we invert them to make chronological plotting more facile
        commits_timestamps = commits_timestamps[::-1]
        commits_timestamps = np.array(commits_timestamps)
        commits_timestamps.sort()

        lower_bound = number_of_commits - len(commits_timestamps) + 1

        return commits_timestamps, lower_bound, number_of_commits

    except GithubException as error:

        if error.status == 404:
            return None, None, None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo = github_client.get_repo(repository_name)

                commits           = repo.get_commits()
                number_of_commits = commits.totalCount

                # get the commit timestamps
                counter = 0
                commits_timestamps = []

                for commit in commits:
                    if commit.commit is not None:
                        commits_timestamps.append(commit.commit.author.date)
                        counter += 1

                        if counter == max_commit_number:
                            break

                # the commits are given from newer to older so we invert them
                # to make chronological plotting more facile
                commits_timestamps = commits_timestamps[::-1]
                commits_timestamps = np.array(commits_timestamps)
                commits_timestamps.sort()

                lower_bound = number_of_commits - len(commits_timestamps) + 1

                return commits_timestamps, lower_bound, number_of_commits

            # for when the api server didn't recover, or for when a socket timeout occurs
            # or for 409: 'Git Repository is empty'
            except:
                return None, None, None


'''
Trail run to ensure proper functioning
'''
if __name__ == "__main__":

    # the csv is used to get some repository names
    data = pd.read_csv('../data/repositories-timeseries.csv', usecols = ['Name with Owner'], index_col = False)

    g = Github("add your github api key here")

    iterations = 0

    for name in data['Name with Owner']:

        timestamps, lower, higher = get_commits_timestamps(g, name, max_commit_number = 250)
        print('-' * 100)
        print(name)

        if lower is not None:
            print('lower bound: {}, total number of commits: {}'.format(lower, higher))

        iterations += 1
        if iterations == 3000:
            break


    '''
    to plot something:
    ----------------------------------------------------------------------------
    import matplotlib.pyplot as plt

    plt.plot(timestamps, range(lower, higher + 1))
    plt.show()
    ----------------------------------------------------------------------------
    '''
