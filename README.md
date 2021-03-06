# pyjam

Version: 0.3.2

## About

`pyjam` is a CLI tool to deploy static sites to AWS. It can sync to an S3 bucket, and configuring it for static site hosting. It can also optionally configure Route53, ACM SSL Certificate and CloudFront.

Serving static site with rich functionalities from a CDN is the basis of the JAM stack. Find out more about the JAM stack here: [https://jamstack.org/](https://jamstack.org/)

This project is based on [acloud.guru](acloud.guru)'s course Automating AWS with Python's project. Additional features include improved error handling, cleaner API, better S3 syncing, setup for SSL certificates, and properly configured CloudFront for S3 website hosting.

## Installation

To install the package, use `pip3` by running `pip3 install pyjam`.

Then, run `jam --help` and you are all set!

## Quick Start

To deploy a static site to AWS using `pyjam`, make sure you have an AWS account and purchase a domain name on Route53. Also, check that you can make a S3 bucket of the same name, by running `jam setup bucket <domain-name>`.

Next, upload your static site contents by running `jam sync <path-to-dir> <domain-name>`.

Then, setup CloudFront content delivery simply by running `jam setup cloudfront <domain-name>`.

Configure your Route53 DNS to point to CloudFront by running `jam setup domain <domain-name> --cf`.

Finally, request a SSL certificate using `jam setup certificate <domain-name>`, and you are all set!

## Commands

`jam list buckets` - Lists all S3 buckets

`jam list bucket <bucket-name>` - Lists all objects in an S3 bucket

`jam setup bucket <bucket-name>` - Create and configure an S3 bucket for static site hosting. Only configures the bucket if it already exists.

- `--region` specifies the AWS region to setup the S3 bucket.

`jam setup domain <domain-name>` - Create and configure a Route53 domain records for S3 or CloudFront.

- `--s3`: create records to point to S3 hosted website with corresponding domain name. NOTE: bucket name must be the same as domain name.

- `--cf`: create records to point a CloudFront distribution. NOTE: distribution CNAME must point to the domain name.

`jam setup certificate <domain-name>` - Create and configure an ACM certificate to use for CloudFront distribution. Works with Route53 issued domain names.

`jam setup cloudfront <bucket-name>` - Create and configure a CloudFront distribution to cache a S3 hosted static website.

`jam sync <path-name> <bucket-name>` - Sync file directory recursively to S3 bucket. Removes stale files and checks for unnecessary uploads.

## Options

`--profile` specifies the AWS profile to use as credentials.

## Configuring for Development

Run `pipenv install` in the file directory.

If you don't yet have `pipenv`, install at [https://pipenv.readthedocs.io/en/latest/](https://pipenv.readthedocs.io/en/latest/)

Use the standard configuration on the AWS CLI. e.g. `aws configure` and add your Access and Secret keys.

The profile should be an AWS power user (more restrictive permissions pending).
