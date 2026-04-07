#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOI 论文元数据获取工具
通过 Crossref API 获取正式出版的学术期刊、会议论文的结构化元数据，
以支持生成符合 IEEE、APA 标准的引文。
"""

import urllib.request
import urllib.error
import json
import argparse
import sys

def fetch_doi_metadata(dois, output_format="json"):
    results = []
    
    # 推荐在请求头中加入联系邮箱，Crossref 会将其分配至更快的 Polite pool
    headers = {
        'User-Agent': 'Trae-Reference-Organizer/1.0 (mailto:admin@example.com)'
    }

    for doi in dois:
        url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read())
                msg = data.get('message', {})
                
                # 提取核心字段
                title = msg.get('title', ['Unknown'])[0]
                container_title = msg.get('container-title', [''])[0]  # 期刊名或会议名
                
                # 作者处理
                authors = []
                for author in msg.get('author', []):
                    given = author.get('given', '')
                    family = author.get('family', '')
                    full_name = f"{given} {family}".strip()
                    if full_name:
                        authors.append(full_name)
                
                # 出版日期处理 (优先取 print，其次 online)
                published = msg.get('published-print', msg.get('published-online', {}))
                date_parts = published.get('date-parts', [[None]])[0]
                year = date_parts[0] if len(date_parts) > 0 and date_parts[0] else 'Unknown'
                month = date_parts[1] if len(date_parts) > 1 and date_parts[1] else 'Unknown'
                
                # 卷期页处理
                volume = msg.get('volume', '')
                issue = msg.get('issue', '')
                page = msg.get('page', '')
                pub_type = msg.get('type', 'Unknown')
                publisher = msg.get('publisher', '')
                
                results.append({
                    'doi': doi,
                    'type': pub_type, # 如 'journal-article', 'proceedings-article'
                    'title': title,
                    'container_title': container_title,
                    'authors': authors,
                    'publisher': publisher,
                    'year': year,
                    'month': month,
                    'volume': volume,
                    'issue': issue,
                    'page': page,
                    'url': msg.get('URL', f"https://doi.org/{doi}")
                })
                
        except urllib.error.HTTPError as e:
            print(f"[{doi}] 请求失败: HTTP {e.code} - 找不到该 DOI 或服务器拒绝访问", file=sys.stderr)
        except Exception as e:
            print(f"[{doi}] 发生未知错误: {e}", file=sys.stderr)
            
    if output_format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif output_format == "text":
        for r in results:
            print(f"DOI: {r['doi']}")
            print(f"Type: {r['type']}")
            print(f"Title: {r['title']}")
            print(f"Container (Journal/Conf): {r['container_title']}")
            print(f"Authors: {', '.join(r['authors'])}")
            print(f"Year: {r['year']} | Vol: {r['volume']} | Issue: {r['issue']} | Page: {r['page']}")
            print("-" * 40)

def main():
    parser = argparse.ArgumentParser(
        description="学术论文 DOI 元数据获取工具 (通过 Crossref API)",
        epilog="示例: python3 .trae/skills/reference-organizer/scripts/doi_metadata_fetcher.py -i 10.1109/TSP.2023.3263000 -f json"
    )
    
    parser.add_argument(
        "-i", "--dois",
        nargs="+",
        required=True,
        help="一个或多个 DOI 标识符，用空格分隔 (例如: 10.1109/TVT.2022.3210570)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json"],
        default="json",
        help="输出格式：json (默认), text"
    )
    
    args = parser.parse_args()
    
    valid_dois = [doi.strip() for doi in args.dois if doi.strip()]
    if not valid_dois:
        print("错误: 请提供有效的 DOI。", file=sys.stderr)
        sys.exit(1)
        
    fetch_doi_metadata(valid_dois, output_format=args.format)

if __name__ == "__main__":
    main()
