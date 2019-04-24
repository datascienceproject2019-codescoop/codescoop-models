import time
import numpy as np
import pandas as pd
from github import Github
from github import GithubException
from datetime import datetime


def get_issues_timestamps(github_client, repository_name, max_open_issues = 200, max_closed_issues = 200):
    '''
    Returns:
        - open issue create timestamps for the specified repository
        - lower bound of number of open issues to be plotted
        - total number of open issues for that repository(higher bound of number of open issues to be plotted)
        - average daily number of open issues

        - closed issue closed timestamps for the specified repository
        - lower bound of number of closed issues to be plotted
        - total number of closed issues for the repository
        - average daily number of closed issues

    max_open_issues: maximum number of entries that shall be returned(if the repository has fewer
                     open issues than all the available ones will be returned)
    max_closed_issues: maximum number of entries that shall be returned(if the repository has fewer
                       closed issues than all the available ones will be returned)
    '''

    try:
        repo = github_client.get_repo(repository_name)

        open_issues           = repo.get_issues(state = 'open')
        number_of_open_issues = open_issues.totalCount

        closed_issues           = repo.get_issues(state = 'closed')
        number_of_closed_issues = closed_issues.totalCount

        # get the open issues timestamps (creation time)
        counter_open = 0
        open_issues_timestamps = []

        for issue in open_issues:
            open_issues_timestamps.append(issue.created_at)
            counter_open += 1

            if counter_open == max_open_issues:
                break

        # the open issues are given from newer to older so we invert them to make chronological plotting more facile
        open_issues_timestamps = open_issues_timestamps[::-1]
        open_issues_timestamps = np.array(open_issues_timestamps)
        open_issues_timestamps.sort()

        lower_open = number_of_open_issues - len(open_issues_timestamps) + 1

        # get the average number of issues opened per day
        try:
            average_open = len(open_issues_timestamps) / ((open_issues_timestamps[-1] - open_issues_timestamps[0]).days)
        except:
            average_open = len(open_issues_timestamps)

        # get the closed issues timestamps (closure time)
        counter_closed = 0
        closed_issues_timestamps = []

        for issue in closed_issues:
            closed_issues_timestamps.append(issue.created_at)
            counter_closed += 1

            if counter_closed == max_closed_issues:
                break

        # the closed issues are given from newer to older so we invert them to make chronological plotting more facile
        closed_issues_timestamps = closed_issues_timestamps[::-1]
        closed_issues_timestamps = np.array(closed_issues_timestamps)
        closed_issues_timestamps.sort()

        lower_closed = number_of_closed_issues - len(closed_issues_timestamps) + 1

        # get the average number of closed issues per day
        try:
            average_closed = len(closed_issues_timestamps) / ((closed_issues_timestamps[-1] - closed_issues_timestamps[0]).days)
        except:
            average_closed = len(closed_issues_timestamps)

        return open_issues_timestamps, lower_open, number_of_open_issues, average_open, closed_issues_timestamps, lower_closed, number_of_closed_issues, average_closed

    except GithubException as error:

        if error.status == 404:
            return None, None, None, None, None, None, None, None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo = github_client.get_repo(repository_name)

                open_issues           = repo.get_issues(state = 'open')
                number_of_open_issues = open_issues.totalCount

                closed_issues           = repo.get_issues(state = 'closed')
                number_of_closed_issues = closed_issues.totalCount

                # get the open issues timestamps (creation time)
                counter_open = 0
                open_issues_timestamps = []

                for issue in open_issues:
                    open_issues_timestamps.append(issue.created_at)
                    counter_open += 1

                    if counter_open == max_open_issues:
                        break

                # the open issues are given from newer to older so we invert them to make chronological plotting more facile
                open_issues_timestamps = open_issues_timestamps[::-1]
                open_issues_timestamps = np.array(open_issues_timestamps)
                open_issues_timestamps.sort()

                lower_open = number_of_open_issues - len(open_issues_timestamps) + 1

                # get the average number of issues opened per day
                try:
                    average_open = len(open_issues_timestamps) / ((open_issues_timestamps[-1] - open_issues_timestamps[0]).days)
                except:
                    average_open = len(open_issues_timestamps)

                # get the closed issues timestamps (closure time)
                counter_closed = 0
                closed_issues_timestamps = []

                for issue in closed_issues:
                    closed_issues_timestamps.append(issue.created_at)
                    counter_closed += 1

                    if counter_closed == max_closed_issues:
                        break

                # the closed issues are given from newer to older so we invert them to make chronological plotting more facile
                closed_issues_timestamps = closed_issues_timestamps[::-1]
                closed_issues_timestamps = np.array(closed_issues_timestamps)
                closed_issues_timestamps.sort()

                lower_closed = number_of_closed_issues - len(closed_issues_timestamps) + 1

                # get the average number of closed issues per day
                try:
                    average_closed = len(closed_issues_timestamps) / ((closed_issues_timestamps[-1] - closed_issues_timestamps[0]).days)
                except:
                    average_closed = len(closed_issues_timestamps)

                return open_issues_timestamps, lower_open, number_of_open_issues, average_open, closed_issues_timestamps, lower_closed, number_of_closed_issues, average_closed


            # for when the api server didn't recover, or for when a socket timeout occurs
            # or for 409: 'Git Repository is empty'
            except:
                return None, None, None, None, None, None, None, None


'''
Trial run to check that everything works as intended
'''
if __name__ == "__main__":

    # the csv is used to get some repository names
    data = pd.read_csv('../data/repositories-timeseries.csv', usecols = ['Name with Owner'], index_col = False)

    g = Github("1deaaa8ea3908191b41f36b1fdaa5567470634fb")

    iterations = 0

    for name in data['Name with Owner']:

        open_issues_timestamps, lower_open, \
            number_of_open_issues, average_open, \
            closed_issues_timestamps, lower_closed, \
            number_of_closed_issues, average_closed = get_issues_timestamps(g, name, max_open_issues = 250, max_closed_issues = 250)
        print('-' * 100)
        print(name)

        if lower_open is not None:
            print('open: lower bound: {}, total number of commits: {}'.format(lower_open, number_of_open_issues))
            print('open: daily average: {}'.format(average_open))
        if lower_closed is not None:
            print('closed: lower bound: {}, total number of commits: {}'.format(lower_closed, number_of_closed_issues))
            print('closed: daily average: {}'.format(average_closed))

        iterations += 1
        if iterations == 3000:
            break


    '''
    to plot something:
    ----------------------------------------------------------------------------
    import matplotlib.pyplot as plt

    plt.plot(open_issues_timestamps, range(lower_open, number_of_open_issues + 1))
    plt.show()
    ----------------------------------------------------------------------------
    '''
