import argparse
from bs4 import BeautifulSoup
import re
import requests


class Solution:
    def __init__(self):
        self._filename = None  # 0
        self._lang = None  # 1
        self._pcode = None  # 2
        self._sid = None  # 4
        self._sres = None  # 5
        self._stime = None  # 6
        self._smem = None  # 7
        self._username = None

    def __repr__(self):

        template = (
            "  -{: ^12.12s}-{: ^10.10s}-{: ^10.10s}-{: ^8.8s}-"
            "{: ^20.20s}-{: ^5.5s}-{: ^5.5s}"
        ).format(
            "filename",
            "lang",
            "pcode",
            "id",
            "result",
            "time",
            "mem")
        sol_stats = (
            "  -{: ^12.12s}-{: ^10.10s}-{: ^10.10s}-{: ^8.8s}-"
            "{: ^20.20s}-{: ^5.5s}-{: ^5.5s}"
        ).format(
            str(self._filename),
            str(self._lang),
            str(self._pcode),
            str(self._sid),
            str(self._sres),
            str(self._stime),
            str(self._smem))
        return "{0}\n{1}".format(template, sol_stats)

    def get_sid(self):
        return self._sid

    def set_sid(self, sid):
        self._sid = sid

    def get_stime(self):
        return self._stime

    def set_stime(self, stime):
        self._stime = stime

    def get_sres(self):
        return self._sres

    def set_sres(self, sres):
        self._sres = sres

    def get_smem(self):
        return self._smem

    def set_smem(self, smem):
        self._smem = smem

    def get_filename(self):
        return self._filename

    def set_filename(self, filename):
        self._filename = filename

    def get_lang(self):
        return self._lang

    def set_lang(self, lang):
        self._lang = lang

    def get_pcode(self):
        return self._pcode

    def set_pcode(self, pcode):
        self._pcode = pcode

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username



def disqualify(sol):
    assert isinstance(sol, Solution)
    pass

def status(sol):
    assert isinstance(sol, Solution)

    resp = requests.get(
        "http://www.spoj.com/status/{},{}/".format(
            sol.get_pcode(),
            sol.get_username()))
    soup = BeautifulSoup(resp.content, 'lxml')
    prob = soup.find("tr", attrs={"class": re.compile("^kol")})
    sol.set_sid(
        prob.find(attrs={'class': 'statustext'}).text.strip()
    )
    res = prob.find(attrs={'id': 'statusres_{}'.format(sol.get_sid())})
    if res["final"] == '1':
        sol.set_sres(
            res["status"]
        )
    else:
        return sol
    sol.set_stime(prob.find(
        attrs={'id': 'statustime_{}'.format(sol.get_sid())}).text.strip())
    sol.set_smem(prob.find(
        attrs={'id': 'statusmem_{}'.format(sol.get_sid())}).text.strip())


def submit(sol, session):
    assert isinstance(sol, Solution)
    assert isinstance(session, requests.Session)
    files = {
        "subm_file": open(sol.get_filename(), 'rb')
    }
    data = {
        "lang": sol.get_lang(),
        "problemcode": sol.get_pcode()
    }
    # let's post it
    response = session.post(
        "http://www.spoj.com/submit/complete/",
        files=files,
        data=data
    )
    if "Solution submitted!" not in response.content:
        raise RuntimeError("Solution couldn't be submitted")

    return response


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        help="turn on verbosity",
        action="store_true"
    )
    parser.add_argument(
        "-i",
        "--inputfile",
        help="solution file to upload",
        required=True
    )
    parser.add_argument(
        "-c",
        "--code",
        help="problem code",
        required=True
    )
    parser.add_argument(
        "-l",
        "--lang",
        type=int,
        help="language code",
        required=True
    )
    parser.add_argument(
        "-u",
        "--username",
        help="spoj username",
        required=True
    )
    parser.add_argument(
        "-p",
        "--password",
        help="spoj password",
        required=True
    )
    args = parser.parse_args()
    return args


def login(username, password, session):
    session.post(
        "https://www.spoj.com/",
        data={
            "login_user": username,
            "password": password
        }
    )
    # have to be done this way 'cause the damn spoj
    # never sends other than 200 except if you really
    # went to nowhere
    myaccount = session.get("http://www.spoj.com/myaccount/")
    if username not in myaccount.content:
        raise RuntimeError("username and password mismatch")


def main():
    args = getargs()
    session = requests.Session()
    login(
        args.username,
        args.password,
        session
    )
    solution = Solution()
    solution.set_username(
        args.username)
    solution.set_filename(
        args.inputfile)
    solution.set_lang(
        args.lang)
    solution.set_pcode(
        args.code)
    submit(solution, session)
    while raw_input("refresh?(y|n) ") == 'y':
        status(solution)
        if solution.get_sres:
            break
        print solution
    print solution
    disqualify(solution)
