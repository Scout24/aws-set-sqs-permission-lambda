from pybuilder.core import use_plugin, init, Author
from pybuilder.vcs import VCSRevision

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin('python.integrationtest')
#use_plugin("pypi:pybuilder_aws_plugin")


name = "aws-set-sqs-permission-lambda"
version = "0.1"
summary = "aws-set-sqs-permission-lambda - Set SQS queue permissions for all ultimiate source of accounts (usofa)"
description = """
    Set SQS queue permissions for all ultimiate source of accounts (usofa)
    """
authors = [Author("Enrico Heine", "enrico.heine@immobilienscout24.de"),
           Author("Tobias Vollmer", "tobias.vollmer@immobilienscout24.de"),
           Author("Tobias Hoeynck", "tobias.hoeynck@immobilienscout24.de")]
url = "https://github.com/ImmobilienScout24/aws-set-sqs-permission-lambda"
license = "Apache License 2.0"
default_task = ["clean", "analyze", "package"]


@init
def set_properties(project):
    project.build_depends_on("boto3")
    project.build_depends_on("moto")
    project.build_depends_on("unittest2")
    project.build_depends_on("simplejson")
    project.set_property("coverage_threshold_warn", 50)
    project.set_property("bucket_name", "aws-set-sqs-permission-lambda")
    project.set_property("lambda_file_access_control", "private")
    project.set_property('integrationtest_inherit_environment', True)
    project.set_property('integrationtest_always_verbose', True)
