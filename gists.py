# -*- coding:utf-8 -*-
""" Gists.py - Script to check new gists"""
import json
from datetime import datetime
import requests
import pickledb
import click

def get_req(url):
    """Gets results from given url"""
    try:
        headers = {'accept':'application/json', 'Content-Type':'application/json'}
        req = requests.get(url=url, headers=headers)
        if req.status_code == 200:
            results = json.loads(req.text)
            return results, req
        else:
            req.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("get_req error: {0} {1}".format(err, req.text))
        return req, req

@click.command()
@click.option('-user', help="Gitbhub username", prompt=True)
def main(user):
    """Function that gets user uname, checks user against Pickle DB and handles gists info"""
    user = user.strip()
    url = "https://api.github.com/users/{}/gists".format(user)
    results, req = get_req(url)
    status = req.status_code
    if status == 200:
        gist_db = pickledb.load('gists.db', True)
        user_data = gist_db.get(user)
        #print("user_data:\n{}\n".format(user_data))
        #print(results)
        if results:
            if user_data:
                gist_date = user_data.get("gist_date")
                gist_date_formatted = datetime.strptime(str(gist_date), "%Y-%m-%dT%H:%M:%SZ")
                new_request_gist_date = datetime.strptime(results[0]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                diff_time = (new_request_gist_date-gist_date_formatted).total_seconds()
                #print(diff_time)
                if diff_time <= 0:
                    print("No new published gists")

                elif diff_time > 0:
                    print("User has published new gist:\nLatest Gist:\n{}".format(results[0]["html_url"]))
                    data = {}
                    data['user'] = user
                    data['gist_date'] = results[0]["created_at"]
                    gist_db.set(str(user), data)

            else:
                print("New user, saving user's details and gists")
                data = {}
                data['user'] = user
                data['gist_date'] = results[0]["created_at"]
                gist_db.set(str(user), data)
        else:
            print("User has no published gists")

    elif status == 404:
        print("Provided Github user doesn't exist")

    else:
        print("Error:\n{}".format(req.text))



if __name__ == '__main__':
    main()
