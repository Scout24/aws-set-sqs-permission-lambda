from pybuilder.core import use_plugin, init, Author
import os

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin('python.integrationtest')
use_plugin("pypi:pybuilder_aws_plugin")


name = "aws-set-sqs-permission-lambda"
version = "0.1"
summary = "aws-set-sqs-permission-lambda - Set SQS queue permissions for all ultimate source of accounts (usofa)"
description = """
    Set SQS queue permissions for all ultimate source of accounts (usofa)
    """
authors = [Author("Enrico Heine", "enrico.heine@immobilienscout24.de"),
           Author("Tobias Vollmer", "tobias.vollmer@immobilienscout24.de"),
           Author("Tobias Hoeynck", "tobias.hoeynck@immobilienscout24.de")]
url = "https://github.com/ImmobilienScout24/aws-set-sqs-permission-lambda"
license = "Apache License 2.0"
default_task = ["clean", "analyze", "package"]


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    project.set_property('teamcity_output', True)
    project.set_property('teamcity_parameter', 'crassus_filename')
    project.set_property('lambda_file_access_control', os.environ.get('LAMBDA_FILE_ACCESS_CONTROL'))
    project.set_property('template_file_access_control', os.environ.get('LAMBDA_FILE_ACCESS_CONTROL'))
    project.set_property("bucket_name", os.environ.get('BUCKET_NAME_FOR_UPLOAD'))
    project.set_property('install_dependencies_index_url',
                         os.environ.get('PYPIPROXY_URL'))
    project.set_property('template_files', [
        ('cfn-sphere/templates', 'aws-set-sqs-permission-lambda.yaml'),
    ])


@init
def set_properties(project):
    project.depends_on("pils")
    project.build_depends_on("boto3")
    project.build_depends_on("moto")
    project.build_depends_on("unittest2")
    project.build_depends_on("simplejson")
    project.build_depends_on("mock")
    project.set_property("coverage_threshold_warn", 50)
    project.set_property("bucket_name", "aws-set-sqs-permission-lambda")
    project.set_property("lambda_file_access_control", "private")
    project.set_property('integrationtest_inherit_environment', True)
    project.set_property('integrationtest_always_verbose', True)
