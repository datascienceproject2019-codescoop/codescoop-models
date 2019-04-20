import time
import pandas as pd
import numpy as np
from github import Github
from github import GithubException
from datetime import datetime


LOWER_BOUND           = 1.791759469228055
UPPER_BOUND           = 42.40071186221785
TIMESTAMP_LOWER_BOUND = "2012-12-12 17:51:25"


'''
Create some np arrays that contains chronological data for a repository:
    - stars count:        get_stars_count_timeseries(dataframe, github_client, repository_name)
    - forks count:        get_forks_count_timeseries(dataframe, github_client, repository_name)
    - watchers count:     get_watchers_count_timeseries(dataframe, github_client, repository_name)
    - contributors count: get_contributors_count_timeseries(dataframe, github_client, repository_name)
    - rating:             get_rating_timeseries(dataframe, github_client, repository_name)

The intended dataframe is the one stored in: ../data/repositories-timeseries.csv

The np arrays can be composed of either four or five elements:
    - the first four are the historical data points of the repository
    - the fifth point is fetched via the github api; this can most likely fail due to:
            - error 404: the repository does not exist anymore
            - error 502: temporary github api problem
            - exceeded the api call limit


Note: it is assumed that the repository name that is given as a input to the fuctions
      does actually exist in the dataframe
'''


def _get_stars_count(github_client, repository_name):
    '''
    Get the Stars Count for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)
        count = repo.stargazers_count

        return count

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)
                count = repo.stargazers_count

                return count

            except GithubException as error:
                return None


def _get_forks_count(github_client, repository_name):
    '''
    Get the Forks Count for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)
        count = repo.forks_count

        return count

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)
                count = repo.forks_count

                return count

            except GithubException as error:
                return None


def _get_watchers_count(github_client, repository_name):
    '''
    Get the Watchers Count for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)
        count = repo.subscribers_count

        return count

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)
                count = repo.subscribers_count

                return count

            except GithubException as error:
                return None


def _get_contributors_count(github_client, repository_name):
    '''
    Get the Contributors Count for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)
        count = repo.get_contributors().totalCount

        return count

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)
                count = repo.get_contributors().totalCount

                return count

            except GithubException as error:
                return None


def _get_rating(github_client, repository_name):
    '''
    Determine the Rating for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)

        star_count        = repo.stargazers_count
        fork_count        = repo.forks_count
        contributor_count = repo.get_contributors().totalCount
        watchers_count    = repo.subscribers_count
        open_issues       = repo.get_issues(state = 'open').totalCount

        updated_timestamp = repo.updated_at
        upd_timestamp = (updated_timestamp - datetime.strptime(TIMESTAMP_LOWER_BOUND, '%Y-%m-%d %H:%M:%S')).days

        has_pages = 0
        for branch in repo.get_branches():
            if branch.name == "gh-pages":
                has_pages = 1

                break

        rating = has_pages + int(repo.has_issues) + int(repo.has_wiki) - int(repo.fork) +\
                 np.log(star_count + 1) + np.log(fork_count + 1) + np.log(contributor_count + 1) +\
                 np.log(watchers_count + 1) - np.log(open_issues + 1) + np.log(upd_timestamp + 1)
        rating = (rating - LOWER_BOUND) / (UPPER_BOUND - LOWER_BOUND)
        rating = round(rating * 5, 2)

        if rating > 5:
            rating = 5
        elif rating < 0:
            rating = 0

        return rating

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)

                star_count        = repo.stargazers_count
                fork_count        = repo.forks_count
                contributor_count = repo.get_contributors().totalCount
                watchers_count    = repo.subscribers_count
                open_issues       = repo.get_issues(state = 'open').totalCount

                updated_timestamp = repo.updated_at
                upd_timestamp = (updated_timestamp - datetime.strptime(TIMESTAMP_LOWER_BOUND, '%Y-%m-%d %H:%M:%S')).days

                has_pages = 0
                for branch in repo.get_branches():
                    if branch.name == "gh-pages":
                        has_pages = 1

                        break

                rating = has_pages + int(repo.has_issues) + int(repo.has_wiki) - int(repo.fork) +\
                         np.log(star_count + 1) + np.log(fork_count + 1) + np.log(contributor_count + 1) +\
                         np.log(watchers_count + 1) - np.log(open_issues + 1) + np.log(upd_timestamp + 1)
                rating = (rating - LOWER_BOUND) / (UPPER_BOUND - LOWER_BOUND)
                rating = round(rating * 5, 2)

                if rating > 5:
                    rating = 5
                elif rating < 0:
                    rating = 0

                return rating

            except GithubException as error:
                return None


def get_stars_count_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Stars Count Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Stars Count_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Stars Count_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Stars Count_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Stars Count_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        stars_count = _get_stars_count(github_client, repository_name)

        if stars_count is not None:
            timeseries = np.append(timeseries, stars_count)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_forks_count_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Forks Count Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Forks Count_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Forks Count_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Forks Count_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Forks Count_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        forks_count = _get_forks_count(github_client, repository_name)

        if forks_count is not None:
            timeseries = np.append(timeseries, forks_count)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_watchers_count_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Watchers Count Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Watchers Count_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Watchers Count_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Watchers Count_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Watchers Count_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        watchers_count = _get_watchers_count(github_client, repository_name)

        if watchers_count is not None:
            timeseries = np.append(timeseries, watchers_count)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_contributors_count_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Contributors Count Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Contributors Count_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Contributors Count_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Contributors Count_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Contributors Count_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        contributors_count = _get_contributors_count(github_client, repository_name)

        if contributors_count is not None:
            timeseries = np.append(timeseries, contributors_count)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_rating_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Rating Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Rating_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Rating_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Rating_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Rating_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        rating = _get_rating(github_client, repository_name)

        if rating is not None:
            timeseries = np.append(timeseries, rating)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries



'''
Trial run to make sure everything works as intended
'''

if __name__ == "__main__":

    data = pd.read_csv("../data/repositories-timeseries.csv", sep = ",", index_col = False)

    g = Github("add github api key here")

    iterations = 0

    for name in data['Name with Owner']:
        print("-" * 100)
        print(name)
        print(get_stars_count_timeseries(data, g, name))
        print(get_forks_count_timeseries(data, g, name))
        print(get_watchers_count_timeseries(data, g, name))
        print(get_contributors_count_timeseries(data, g, name))
        print(get_rating_timeseries(data, g, name))

        iterations += 1

        if iterations == 2000:
            break
