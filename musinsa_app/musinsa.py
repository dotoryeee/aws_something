# you can choose 'old date threshold=5' like this -> eg. python3 musinsa.py 5
# this code work with aws credential profile[musinsa] in your server(~/.aws/credentials)

import boto3
import datetime
import csv
import argparse
import botocore.exceptions


try:
    session = boto3.Session(profile_name="musinsa")
    print("Credential file loaded")
    iam = session.client("iam")
except botocore.exceptions.ProfileNotFound:
    print("NO CREDENTIAL FOUND")
except Exception as e:
    print(f"FAIL: load credentials {e}")


def getArgs():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "old", help="insert 'old' threshold(int)", type=int, default=0, nargs="?"
        )
        args = parser.parse_args()
        print(f"select accesskeys older than {args.old} day(s)")
        return args.old
    except Exception as e:
        print(f"FAIL: arg parser {e}")


def getUserList():
    user_names = []
    try:
        iam_users = iam.list_users()["Users"]
        for user in iam_users:
            user_names.append(user["UserName"])
        return user_names
    except Exception as e:
        print(f"FAIL: get user list{e}")


def getAccessKeys(user_names):
    access_key_list = []
    try:
        for user_name in user_names:
            paginator = iam.get_paginator("list_access_keys")
            for response in paginator.paginate(UserName=user_name):
                try:
                    access_key_list.append(
                        response["AccessKeyMetadata"][0]
                    )  # User's fisrt access key
                    access_key_list.append(
                        response["AccessKeyMetadata"][1]
                    )  # User's second access key
                except:
                    pass  # pass if user don't have access key
        return access_key_list
    except Exception as e:
        print(f"FAIL: get access key info{e}")


def appendHowOld(access_key_list, old_target):
    returnData = []
    today = datetime.datetime.now(datetime.timezone.utc)
    try:
        for access_key_info in access_key_list:
            date_diff = today - access_key_info["CreateDate"]
            if date_diff.days >= old_target:
                access_key_info["HowOld"] = date_diff.days
                returnData.append(access_key_info)
        return returnData
    except Exception as e:
        print(f"FAIL: append accesskey old info{e}")


def makeCSV(access_key_list):
    try:
        f = open("AccessKeyList.csv", "w")
        writer = csv.writer(f)
        writer.writerow(["UserName", "AccessKeyId", "CreateDate", "HowOld"])
        for ak in access_key_list:
            writer.writerow(
                [
                    ak["UserName"],
                    ak["AccessKeyId"],
                    ak["CreateDate"].strftime("%Y-%m-%d"),
                    ak["HowOld"],
                ]
            )
        f.close()
        return "success"
    except Exception as e:
        print(f"FAIL: making CSV {e}")


if __name__ == "__main__":
    old_target = getArgs()
    user_names = getUserList()
    access_key_list = getAccessKeys(user_names)
    access_key_list = appendHowOld(access_key_list, old_target)
    make_file_result = makeCSV(access_key_list)
    print(make_file_result)
