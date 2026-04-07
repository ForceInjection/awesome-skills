#!/usr/bin/env python3
import sys
import argparse

def search_icon(query):
    """
    Search for architecture icons based on a simple query.
    Returns a dictionary with the draw.io icon style name, color, and type.
    """
    mapping = {
        # --- AWS Compute (Orange: #F58536) ---
        "ec2": {"type": "aws", "icon": "mxgraph.aws4.ec2", "color": "#F58536"},
        "lambda": {"type": "aws", "icon": "mxgraph.aws4.lambda", "color": "#F58536"},
        "ecs": {"type": "aws", "icon": "mxgraph.aws4.ecs", "color": "#F58536"},
        "eks": {"type": "aws", "icon": "mxgraph.aws4.eks", "color": "#F58536"},
        "fargate": {"type": "aws", "icon": "mxgraph.aws4.fargate", "color": "#F58536"},
        "elastic beanstalk": {"type": "aws", "icon": "mxgraph.aws4.elastic_beanstalk", "color": "#F58536"},
        "batch": {"type": "aws", "icon": "mxgraph.aws4.batch", "color": "#F58536"},
        
        # --- AWS Storage (Green: #4F81A1) ---
        "s3": {"type": "aws", "icon": "mxgraph.aws4.s3", "color": "#4F81A1"},
        "ebs": {"type": "aws", "icon": "mxgraph.aws4.ebs", "color": "#4F81A1"},
        "efs": {"type": "aws", "icon": "mxgraph.aws4.efs", "color": "#4F81A1"},
        "glacier": {"type": "aws", "icon": "mxgraph.aws4.glacier", "color": "#4F81A1"},
        "storage gateway": {"type": "aws", "icon": "mxgraph.aws4.storage_gateway", "color": "#4F81A1"},
        "fsx": {"type": "aws", "icon": "mxgraph.aws4.fsx", "color": "#4F81A1"},

        # --- AWS Database (Blue: #3355CC) ---
        "rds": {"type": "aws", "icon": "mxgraph.aws4.rds", "color": "#3355CC"},
        "dynamodb": {"type": "aws", "icon": "mxgraph.aws4.dynamodb", "color": "#3355CC"},
        "elasticache": {"type": "aws", "icon": "mxgraph.aws4.elasticache", "color": "#3355CC"},
        "redshift": {"type": "aws", "icon": "mxgraph.aws4.redshift", "color": "#3355CC"},
        "aurora": {"type": "aws", "icon": "mxgraph.aws4.aurora", "color": "#3355CC"},
        "neptune": {"type": "aws", "icon": "mxgraph.aws4.neptune", "color": "#3355CC"},
        "documentdb": {"type": "aws", "icon": "mxgraph.aws4.documentdb", "color": "#3355CC"},

        # --- AWS Networking & Content Delivery (Purple: #8C4FFF) ---
        "vpc": {"type": "aws", "icon": "mxgraph.aws4.vpc", "color": "#8C4FFF"},
        "api gateway": {"type": "aws", "icon": "mxgraph.aws4.api_gateway", "color": "#8C4FFF"},
        "cloudfront": {"type": "aws", "icon": "mxgraph.aws4.cloudfront", "color": "#8C4FFF"},
        "route53": {"type": "aws", "icon": "mxgraph.aws4.route_53", "color": "#8C4FFF"},
        "route 53": {"type": "aws", "icon": "mxgraph.aws4.route_53", "color": "#8C4FFF"},
        "direct connect": {"type": "aws", "icon": "mxgraph.aws4.direct_connect", "color": "#8C4FFF"},
        "elastic load balancing": {"type": "aws", "icon": "mxgraph.aws4.elastic_load_balancing", "color": "#8C4FFF"},
        "elb": {"type": "aws", "icon": "mxgraph.aws4.elastic_load_balancing", "color": "#8C4FFF"},
        "alb": {"type": "aws", "icon": "mxgraph.aws4.elastic_load_balancing", "color": "#8C4FFF"},
        "transit gateway": {"type": "aws", "icon": "mxgraph.aws4.transit_gateway", "color": "#8C4FFF"},

        # --- AWS Security, Identity & Compliance (Dark Navy: #232F3E) ---
        "iam": {"type": "aws", "icon": "mxgraph.aws4.iam", "color": "#232F3E"},
        "cognito": {"type": "aws", "icon": "mxgraph.aws4.cognito", "color": "#232F3E"},
        "kms": {"type": "aws", "icon": "mxgraph.aws4.kms", "color": "#232F3E"},
        "secrets manager": {"type": "aws", "icon": "mxgraph.aws4.secrets_manager", "color": "#232F3E"},
        "shield": {"type": "aws", "icon": "mxgraph.aws4.shield", "color": "#232F3E"},
        "waf": {"type": "aws", "icon": "mxgraph.aws4.waf", "color": "#232F3E"},
        "guardduty": {"type": "aws", "icon": "mxgraph.aws4.guardduty", "color": "#232F3E"},
        "inspector": {"type": "aws", "icon": "mxgraph.aws4.inspector", "color": "#232F3E"},
        "macie": {"type": "aws", "icon": "mxgraph.aws4.macie", "color": "#232F3E"},

        # --- AWS Application Integration (Pink: #E7157B) ---
        "sqs": {"type": "aws", "icon": "mxgraph.aws4.sqs", "color": "#E7157B"},
        "sns": {"type": "aws", "icon": "mxgraph.aws4.sns", "color": "#E7157B"},
        "step functions": {"type": "aws", "icon": "mxgraph.aws4.step_functions", "color": "#E7157B"},
        "eventbridge": {"type": "aws", "icon": "mxgraph.aws4.eventbridge", "color": "#E7157B"},
        "mq": {"type": "aws", "icon": "mxgraph.aws4.mq", "color": "#E7157B"},
        "appsync": {"type": "aws", "icon": "mxgraph.aws4.appsync", "color": "#E7157B"},

        # --- AWS Management & Governance (Magenta: #CC2264) ---
        "cloudwatch": {"type": "aws", "icon": "mxgraph.aws4.cloudwatch", "color": "#CC2264"},
        "cloudtrail": {"type": "aws", "icon": "mxgraph.aws4.cloudtrail", "color": "#CC2264"},
        "config": {"type": "aws", "icon": "mxgraph.aws4.config", "color": "#CC2264"},
        "systems manager": {"type": "aws", "icon": "mxgraph.aws4.systems_manager", "color": "#CC2264"},
        "trusted advisor": {"type": "aws", "icon": "mxgraph.aws4.trusted_advisor", "color": "#CC2264"},

        # --- AWS Analytics (Purple: #8C4FFF) ---
        "athena": {"type": "aws", "icon": "mxgraph.aws4.athena", "color": "#8C4FFF"},
        "emr": {"type": "aws", "icon": "mxgraph.aws4.emr", "color": "#8C4FFF"},
        "kinesis": {"type": "aws", "icon": "mxgraph.aws4.kinesis", "color": "#8C4FFF"},
        "glue": {"type": "aws", "icon": "mxgraph.aws4.glue", "color": "#8C4FFF"},
        "quicksight": {"type": "aws", "icon": "mxgraph.aws4.quicksight", "color": "#8C4FFF"},

        # --- AWS Containers & Dev Tools ---
        "ecr": {"type": "aws", "icon": "mxgraph.aws4.ecr", "color": "#F58536"},
        "codecommit": {"type": "aws", "icon": "mxgraph.aws4.codecommit", "color": "#3355CC"},
        "codebuild": {"type": "aws", "icon": "mxgraph.aws4.codebuild", "color": "#3355CC"},
        "codedeploy": {"type": "aws", "icon": "mxgraph.aws4.codedeploy", "color": "#3355CC"},
        "codepipeline": {"type": "aws", "icon": "mxgraph.aws4.codepipeline", "color": "#3355CC"},
        
        # ==========================================
        # --- KUBERNETES (K8s standard #326CE5) ---
        # ==========================================
        "pod": {"type": "k8s", "icon": "img/lib/kubernetes/compute/pod.svg"},
        "node": {"type": "k8s", "icon": "img/lib/kubernetes/compute/node.svg"},
        "deployment": {"type": "k8s", "icon": "img/lib/kubernetes/compute/deploy.svg"},
        "service": {"type": "k8s", "icon": "img/lib/kubernetes/network/service.svg"},
        "ingress": {"type": "k8s", "icon": "img/lib/kubernetes/network/ing.svg"},
        "configmap": {"type": "k8s", "icon": "img/lib/kubernetes/storage/c-m.svg"},
        "secret": {"type": "k8s", "icon": "img/lib/kubernetes/storage/secret.svg"},
        "pvc": {"type": "k8s", "icon": "img/lib/kubernetes/storage/pvc.svg"},
        "pv": {"type": "k8s", "icon": "img/lib/kubernetes/storage/pv.svg"},
        "statefulset": {"type": "k8s", "icon": "img/lib/kubernetes/compute/sts.svg"},
        "daemonset": {"type": "k8s", "icon": "img/lib/kubernetes/compute/ds.svg"},
        "job": {"type": "k8s", "icon": "img/lib/kubernetes/compute/job.svg"},
        "cronjob": {"type": "k8s", "icon": "img/lib/kubernetes/compute/cronjob.svg"},
        "namespace": {"type": "k8s", "icon": "img/lib/kubernetes/admin/ns.svg"},
        
        # ==========================================
        # --- GENERAL IT / FLOWCHART -----------
        # ==========================================
        "database": {"type": "general", "icon": "cylinder3", "color": "#dae8fc", "stroke": "#6c8ebf"},
        "db": {"type": "general", "icon": "cylinder3", "color": "#dae8fc", "stroke": "#6c8ebf"},
        "user": {"type": "general", "icon": "umlActor", "color": "none", "stroke": "#333333"},
        "actor": {"type": "general", "icon": "umlActor", "color": "none", "stroke": "#333333"},
        "client": {"type": "general", "icon": "umlActor", "color": "none", "stroke": "#333333"},
        "cloud": {"type": "general", "icon": "cloud", "color": "#ffffff", "stroke": "#333333"},
        "internet": {"type": "general", "icon": "cloud", "color": "#ffffff", "stroke": "#333333"},
        "server": {"type": "general", "icon": "mxgraph.cisco.servers.standard_host", "color": "none", "stroke": "none"},
        "component": {"type": "general", "icon": "module", "color": "#f5f5f5", "stroke": "#666666"},
        "module": {"type": "general", "icon": "module", "color": "#f5f5f5", "stroke": "#666666"},
        "browser": {"type": "general", "icon": "mxgraph.mockup.containers.browserWindow", "color": "#ffffff", "stroke": "#666666"},
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
    parser = argparse.ArgumentParser(description="Find official Architecture (AWS/K8s/General) icon styles for draw.io")
    parser.add_argument("service", help="Service or component name (e.g., ec2, pod, database)")
    parser.add_argument("--style", action="store_true", help="Output full XML style string including standard formatting")
    args = parser.parse_args()
    
    result = search_icon(args.service)
    
    if result:
        if args.style:
            # Construct the exact standardized style string based on type
            if result["type"] == "aws":
                style_str = f"shape=mxgraph.aws4.resourceIcon;resIcon={result['icon']};fillColor={result['color']};strokeColor=none;html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
            elif result["type"] == "k8s":
                # K8s icons use the standard draw.io image shape referencing the kubernetes clip art
                style_str = f"shape=image;image={result['icon']};html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
            else: # general
                style_str = f"shape={result['icon']};fillColor={result['color']};strokeColor={result['stroke']};html=1;pointerEvents=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
                
            print(style_str)
        else:
            print(result['icon'])
        sys.exit(0)
    else:
        print(f"Error: Could not find an architecture icon mapping for '{args.service}'.", file=sys.stderr)
        print("You may need to search directly in the draw.io UI.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
