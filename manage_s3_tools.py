#!/usr/bin/env python

"""
This module contains functions that help manage S3 buckets
"""

import boto3
import click


# create a function that counts the total number of buckets in my account
def count_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"]]
    num_of_buckets = len(buckets)
    print(f"You have {num_of_buckets} buckets in your account")
    return num_of_buckets


# create a function that finds all empty buckets in my account
def list_empty_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"]]
    empty_buckets = []
    for bucket in buckets:
        response = s3.list_objects_v2(Bucket=bucket)
        if "Contents" not in response:
            empty_buckets.append(bucket)
    return empty_buckets


# create a function that deletes all buckets that match a pattern
def delete_bucket(pattern):
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"]]
    for bucket in buckets:
        if pattern in bucket:
            s3.delete_bucket(Bucket=bucket)
            print(f"{bucket} deleted")


# create a click group
@click.group()
def cli():
    """manage s3 buckets"""


# create a click subcommand
@cli.command("count")
def count():
    """Count the number of buckets in your account
    Example: ./manage_s3_tools.py count
    """
    count_buckets()


# create a click subcommand
@cli.command("list-empty-buckets")
def list_empty():
    """List all empty buckets in your account
    Example: ./manage_s3_tools.py list-empty-buckets
    """
    empty_buckets = list_empty_buckets()
    print("Empty buckets:")
    for bucket in empty_buckets:
        print(bucket)


# create a click subcommand
@cli.command("delete-buckets")
@click.argument("pattern")
def delete_buckets(pattern):
    """Delete all buckets that match a pattern
    Example: ./manage_s3_tools.py delete-buckets my-bucket-pattern
    """
    delete_bucket(pattern)


if __name__ == "__main__":
    cli()
