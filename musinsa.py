from os import access
import boto3
import datetime
import csv

session = boto3.Session(profile_name="musinsa")
iam = session.client("iam")
today = datetime.datetime.now(datetime.timezone.utc)


def getUserList():
    try:
        user_names = []
        iam_users = iam.list_users()["Users"]
        for user in iam_users:
            user_names.append(user["UserName"])
        return user_names
    except:
        print("FAIL: get uset list")


def getAccessKeys(user_names):
    access_key_list = []
    try:
        for user_name in user_names:
            paginator = iam.get_paginator("list_access_keys")
            for response in paginator.paginate(UserName=user_name):
                try:
                    access_key_list.append(response["AccessKeyMetadata"][0])
                except:
                    pass  # pass if user don't have access key
        return access_key_list
    except:
        print("FAIL: get access key info")


def appendHowOld(access_key_list):
    returnData = []
    try:
        for access_key_info in access_key_list:
            date_diff = today - access_key_info["CreateDate"]
            access_key_info["HowOld"] = date_diff.days
            returnData.append(access_key_info)
        return returnData
    except:
        print("FAIL: append accesskey old info")


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
    except:
        return "FAIL: making CSV"


def main():
    user_names = getUserList()
    access_key_list = getAccessKeys(user_names)
    access_key_list = appendHowOld(access_key_list)
    make_file_result = makeCSV(access_key_list)
    print(make_file_result)


main()
