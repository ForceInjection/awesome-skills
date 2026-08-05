---
name: "reference-organizer"
description: "Fetch metadata for links and generate formatted references at different levels (blogs, whitepapers, papers). Invoke this skill when the user needs to organize references, generate citations, or format reference links."
---

# Reference Organizer

This skill automatically fetches metadata for external links (e.g., blog posts, technical whitepapers, and academic papers) and formats it into standard reference entries at the level and scenario requested by the user. By automating information retrieval and typesetting, it improves the efficiency and professionalism of reference writing in technical articles.

## Applicable Scenarios

Based on different technical writing needs, this skill supports metadata extraction for three primary document types: blog posts, technical whitepapers, and academic papers. These three types cover a broad range of scenarios, from informal experience sharing to rigorous academic argumentation. For each medium, the skill focuses on extracting specific data dimensions to meet citation standards.

- **Blog**: Extract the article title, author, publication date, and link; generate a lightweight reference format suitable for display at the end of a technical article.
- **Whitepaper**: Extract the whitepaper title, publishing organization/company, year, and link; generate a formal reference format.
- **Paper**: Extract the paper title, authors, publication year, and DOI or arXiv link; generate a citation in IEEE, APA, or another academic standard.

## Core Workflow

Processing external links requires a standardized pipeline: from analyzing link characteristics to fetching specific metadata, the entire process is divided into two consecutive stages: identification/extraction and typesetting/output.

### Link Type Identification and Information Retrieval

Accurate metadata extraction depends on identifying the link's host. Academic repositories such as arXiv provide structured API interfaces, while regular web pages require general-purpose fetching tools combined with natural language understanding to extract core information.

- **arXiv preprint papers**:
  - Extract the arXiv ID from the link.
  - Use the Python script provided with the system to fetch metadata and predefined formats:

    ```bash
    # 使用本技能目录下的 Python 脚本获取指定 arXiv 论文的元数据
    # 注意：LLM 在执行命令前，请先使用文件路径相关工具确认本技能目录的绝对路径，并将其替换到 <SKILL_DIR> 中。
    python3 <SKILL_DIR>/scripts/arxiv_metadata_fetcher.py -i <arXiv_ID> -f <format>
    ```

    _(Supported `format` values: `text`, `json`, `markdown`, `ieee`)_

- **Academic journal/conference papers (DOI)**:
  - If the link is a formally published academic paper (commonly found on platforms such as IEEE Xplore, ACM, and Springer), extract the DOI identifier from the link.
  - Use the provided DOI fetching script to obtain structured metadata (via the Crossref API) to cope with publishers' anti-scraping blocking:

    ```bash
    # 获取指定 DOI 的元数据（输出 JSON）
    python3 <SKILL_DIR>/scripts/doi_metadata_fetcher.py -i <DOI> -f json
    ```

- **Regular web pages (blogs, whitepapers, official documentation, etc.)**:
  - Prefer using a web content fetching tool (such as `mcp_DuckDuckGo_Search_Server_fetch_content`) to retrieve the page's body text or metadata.
  - Analyze the fetched content and extract key information: title, author or publishing organization, and publication time.

### Formatting Output Specifications

Once metadata retrieval is complete, map it to the appropriate citation template. To ensure rigorous output, this skill defaults to typesetting with the nationally or internationally recognized standards of the academic and publishing communities: GB/T 7714-2015, APA, and IEEE.

- **Blog/web page level (default: GB/T 7714-2015 electronic resource)**:
  - Format: `[Serial number] [Primary author]. [Title][EB/OL]. ([Update or revision date])[Access date]. [Access path].`
  - Example: `[1] Trae Team. Trae AI IDE Quick Start[EB/OL]. (2023-10-01)[2024-04-04]. https://example.com.`

- **Whitepaper/technical report level (default: APA 7th Edition)**:
  - Format: `[Publishing organization]. ([Publication year]). *[Report title]*. [URL]`
  - Example: `OpenAI. (2023). *GPT-4 technical report*. https://example.com`

- **Paper level (default: IEEE format)**:
  Since paper sources differ, strictly distinguish among the following IEEE sub-formats based on the metadata. **Font requirements in the format**: for formal publications (such as journal and conference names), use Markdown italics `*...*`; for informal publications (such as preprints), use upright (non-italic) type throughout; paper titles must use double quotation marks `"[title],"` with the comma inside the quotation marks.
  - **Journal article**:
    - Format: `[Serial number] [Author (initial. surname)], "[Paper title]," *[Journal name abbreviation]*, vol. [volume], no. [issue], pp. [page range], [month abbreviation]. [year].`
    - Example: `[1] J. Smith and M. Johnson, "Deep learning for signal processing," *IEEE Trans. Signal Process.*, vol. 68, pp. 1234-1245, Mar. 2023.`
  - **Conference paper**:
    - Format: `[Serial number] [Author], "[Paper title]," in *Proc. [Conference name abbreviation]*, [Conference city], [Conference country], [year], pp. [page range].`
    - Example: `[2] K. Lee, "Neural network optimization," in *Proc. IEEE Int. Conf. Mach. Learn.*, Vancouver, Canada, 2023, pp. 567-574.`
  - **Preprint (e.g., arXiv)**:
    - Format: `[Serial number] [Author], "[Paper title]," arXiv preprint arXiv:[ID], [year].`
    - Example: `[3] A. Vaswani et al., "Attention is all you need," arXiv preprint arXiv:1706.03762, 2017.`

## Best Practices and Cautions

To handle extreme cases such as anti-scraping mechanisms, missing information, and high concurrency, and to improve the quality and stability of generated references, strictly follow the practice guidelines below while performing the task.

- **Batch processing**: If the user provides multiple links, extract information from each link one at a time in order (to avoid context state conflicts caused by high-concurrency calls), and output a single, clearly categorized reference list.
- **Missing information**: If author, date, or other information cannot be retrieved due to anti-scraping mechanisms or page structure, mark the output with `[Author unknown]` or `[Date unknown]` and prompt the user to fill in the details manually.
- **Formatting compliance**: Strictly follow Markdown syntax, keep a space between Chinese and English text, wrap proper nouns in backticks, and never use HTML tags such as `<br>` in tables.
