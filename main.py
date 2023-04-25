import argparse
import mysql.connector
import os
import time

from typing import List, Dict


class ArgList:
    host: str
    user: str
    password: str
    endocap: int
    exclude: List[str]


def pars_args() -> ArgList:
    parser = argparse.ArgumentParser()
    parser.add_argument("-h", "--host", help="Database Host",
                        type=str, required=True)
    parser.add_argument(
        "-u", "--user", help="Database Username", type=str, required=True)
    parser.add_argument("-p", "--password",
                        help="Database Password", type=str, required=True)
    parser.add_argument("-e", "--endocap",
                        help="Current Endocap, default = 25", type=int, default=25, required=False)
    parser.add_argument("-x", "--exclude", help="Excluded nations (Delegate, Vice Delegate, etc). Pass this argument multiple times -- once per nation.",
                        action="append", type=str, default=[], required=False)

    args = ArgList()

    parser.parse_args(namespace=args)

    return args


def create_db_connection(host: str, user: str, password: str) -> mysql.connector.MySQLConnection:
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="ns"
    )

    return mydb


def create_tg_list(args: ArgList, conn: mysql.connector.MySQLConnection) -> Dict[str, List[str]]:
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT name, numendos FROM nations WHERE region = 'europeia' AND NOT unstatus = 'Non-Member' ORDER BY numendos DESC"

    cursor.execute(sql)

    nations: Dict[str, int] = {nation["name"]: nation["numendos"]
                               for nation in cursor.fetchall()}

    nations_over_cap: List[str] = [nation for nation,
                                   numendos in nations.items() if numendos > args.endocap and nation not in args.exclude]

    telegram_list: Dict[str, List[str]] = {}

    for nation in nations_over_cap:
        print(f"Getting endorsements for {nation}")
        sql = "SELECT endorsements FROM nations WHERE name = %s"
        val = (nation,)

        cursor.execute(sql, val)

        endorsements = cursor.fetchone()["endorsements"].strip(",").split(",")

        for endorser in endorsements:
            if endorser not in telegram_list:
                telegram_list[endorser] = []

            telegram_list[endorser].append(nation)

        time.sleep(1)

    return telegram_list


def output(telegram_list: Dict[str, List[str]]) -> None:
    with open(f"{os.path.dirname(os.path.realpath(__file__))}\output.txt", "w") as out_file:
        for endorser in telegram_list:
            out_file.write(f"{endorser}:\n")
            out_file.write(
                ", ".join([f"[nation]{nation}[/nation]" for nation in telegram_list[endorser]]))
            out_file.write("\n\n")


def main():
    args = pars_args()

    db_connection = create_db_connection(args.host, args.user, args.password)

    telegram_list = create_tg_list(args, db_connection)

    output(telegram_list)


if __name__ == "__main__":
    main()
