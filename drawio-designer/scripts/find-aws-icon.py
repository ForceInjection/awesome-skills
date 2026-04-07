#!/usr/bin/env python3
import sys
import argparse
import urllib.request
import json
import re

def search_aws_icon(query):
    """
    Search for AWS icons based on a simple query matching commonly used service names.
    Returns a dictionary with the draw.io mxgraph.aws4.* icon style name and its standard AWS category color.
    """
    mapping = {
        # Compute (Orange: #F58536)
        "ec2": {"icon": "mxgraph.aws4.ec2", "color": "#F58536"},
        "lambda": {"icon": "mxgraph.aws4.lambda", "color": "#F58536"},
        "ecs": {"icon": "mxgraph.aws4.ecs", "color": "#F58536"},
        "eks": {"icon": "mxgraph.aws4.eks", "color": "#F58536"},
        "fargate": {"icon": "mxgraph.aws4.fargate", "color": "#F58536"},
        "elastic beanstalk": {"icon": "mxgraph.aws4.elastic_beanstalk", "color": "#F58536"},
        "batch": {"icon": "mxgraph.aws4.batch", "color": "#F58536"},
        
        # Storage (Green: #4F81A1)
        "s3": {"icon": "mxgraph.aws4.s3", "color": "#4F81A1"},
        "ebs": {"icon": "mxgraph.aws4.ebs", "color": "#4F81A1"},
        "efs": {"icon": "mxgraph.aws4.efs", "color": "#4F81A1"},
        "glacier": {"icon": "mxgraph.aws4.glacier", "color": "#4F81A1"},
        "storage gateway": {"icon": "mxgraph.aws4.storage_gateway", "color": "#4F81A1"},
        "fsx": {"icon": "mxgraph.aws4.fsx", "color": "#4F81A1"},

        # Database (Blue: #3355CC)
        "rds": {"icon": "mxgraph.aws4.rds", "color": "#3355CC"},
        "dynamodb": {"icon": "mxgraph.aws4.dynamodb", "color": "#3355CC"},
        "elasticache": {"icon": "mxgraph.aws4.elasticache", "color": "#3355CC"},
        "redshift": {"icon": "mxgraph.aws4.redshift", "color": "#3355CC"},
        "aurora": {"icon": "mxgraph.aws4.aurora", "color": "#3355CC"},
        "neptune": {"icon": "mxgraph.aws4.neptune", "color": "#3355CC"},
        "documentdb": {"icon": "mxgraph.aws4.documentdb", "color": "#3355CC"},

        # Networking & Content Delivery (Purple: #8C4FFF)
        "vpc": {"icon": "mxgraph.aws4.vpc", "color": "#8C4FFF"},
        "api gateway": {"icon": "mxgraph.aws4.api_gateway", "color": "#8C4FFF"},
        "cloudfront": {"icon": "mxgraph.aws4.cloudfront", "color": "#8C4FFF"},
        "route53": {"icon": "mxgraph.aws4.route_53", "color": "#8C4FFF"},
        "route 53": {"icon": "mxgraph.aws4.route_53", "color": "#8C4FFF"},
        "direct connect": {"icon": "mxgraph.aws4.direct_connect", "color": "#8C4FFF"},
        "elastic load balancing": {"icon": "mxgraph.aws4.elastic_load_balancing", "color": "#8C4FFF"},
        "elb": {"icon": "mxgraph.aws4.elastic_load_balancing", "color": "#8C4FFF"},
        "alb": {"icon": "mxgraph.aws4.elastic_load_balancing", "color": "#8C4FFF"},
        "transit gateway": {"icon": "mxgraph.aws4.transit_gateway", "color": "#8C4FFF"},

        # Security, Identity & Compliance (Dark Navy: #232F3E)
        "iam": {"icon": "mxgraph.aws4.iam", "color": "#232F3E"},
        "cognito": {"icon": "mxgraph.aws4.cognito", "color": "#232F3E"},
        "kms": {"icon": "mxgraph.aws4.kms", "color": "#232F3E"},
        "secrets manager": {"icon": "mxgraph.aws4.secrets_manager", "color": "#232F3E"},
        "shield": {"icon": "mxgraph.aws4.shield", "color": "#232F3E"},
        "waf": {"icon": "mxgraph.aws4.waf", "color": "#232F3E"},
        "guardduty": {"icon": "mxgraph.aws4.guardduty", "color": "#232F3E"},
        "inspector": {"icon": "mxgraph.aws4.inspector", "color": "#232F3E"},
        "macie": {"icon": "mxgraph.aws4.macie", "color": "#232F3E"},

        # Application Integration (Pink: #E7157B)
        "sqs": {"icon": "mxgraph.aws4.sqs", "color": "#E7157B"},
        "sns": {"icon": "mxgraph.aws4.sns", "color": "#E7157B"},
        "step functions": {"icon": "mxgraph.aws4.step_functions", "color": "#E7157B"},
        "eventbridge": {"icon": "mxgraph.aws4.eventbridge", "color": "#E7157B"},
        "mq": {"icon": "mxgraph.aws4.mq", "color": "#E7157B"},
        "appsync": {"icon": "mxgraph.aws4.appsync", "color": "#E7157B"},

        # Management & Governance (Magenta: #CC2264)
        "cloudwatch": {"icon": "mxgraph.aws4.cloudwatch", "color": "#CC2264"},
        "cloudtrail": {"icon": "mxgraph.aws4.cloudtrail", "color": "#CC2264"},
        "config": {"icon": "mxgraph.aws4.config", "color": "#CC2264"},
        "systems manager": {"icon": "mxgraph.aws4.systems_manager", "color": "#CC2264"},
        "trusted advisor": {"icon": "mxgraph.aws4.trusted_advisor", "color": "#CC2264"},

        # Analytics (Purple: #8C4FFF)
        "athena": {"icon": "mxgraph.aws4.athena", "color": "#8C4FFF"},
        "emr": {"icon": "mxgraph.aws4.emr", "color": "#8C4FFF"},
        "kinesis": {"icon": "mxgraph.aws4.kinesis", "color": "#8C4FFF"},
        "glue": {"icon": "mxgraph.aws4.glue", "color": "#8C4FFF"},
        "quicksight": {"icon": "mxgraph.aws4.quicksight", "color": "#8C4FFF"},

        # Containers (Orange: #F58536)
        "ecr": {"icon": "mxgraph.aws4.ecr", "color": "#F58536"},
        
        # Developer Tools (Blue: #3355CC)
        "codecommit": {"icon": "mxgraph.aws4.codecommit", "color": "#3355CC"},
        "codebuild": {"icon": "mxgraph.aws4.codebuild", "color": "#3355CC"},
        "codedeploy": {"icon": "mxgraph.aws4.codedeploy", "color": "#3355CC"},
        "codepipeline": {"icon": "mxgraph.aws4.codepipeline", "color": "#3355CC"},
    }
    
    query_lower = query.lower()
    
    # Exact match
    if query_lower in mapping:
        return mapping[query_lower]
        
    # Partial match
    for key, value in mapping.items():
        if query_lower in key or key in query_lower:
            return value
            
    return None

def main():
    parser = argparse.ArgumentParser(description="Find official AWS icon styles for draw.io")
    parser.add_argument("service", help="AWS service name (e.g., ec2, lambda)")
    parser.add_argument("--style", action="store_true", help="Output full XML style string including standard color")
    args = parser.parse_args()
    
    result = search_aws_icon(args.service)
    
    if result:
        if args.style:
            # Construct the exact standardized style string
            style_str = f"shape=mxgraph.aws4.resourceIcon;resIcon={result['icon']};fillColor={result['color']};strokeColor=none;html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
            print(style_str)
        else:
            print(result['icon'])
        sys.exit(0)
    else:
        print(f"Error: Could not find an AWS icon mapping for '{args.service}'.", file=sys.stderr)
        print("You may need to search directly in the draw.io UI.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
