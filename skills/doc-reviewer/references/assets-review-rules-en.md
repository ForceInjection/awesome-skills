# Assets & Links Review Rules (Compliance & Asset Inspector)

The core of this review type is **verifying the validity and content security of the document's external dependencies**.
**Execution strategy**: Globally extract all links, image paths, configuration files, and references from the document and validate them in batch, ensuring the document's "assets" remain intact, compliant, and secure.

- **File and Directory Naming**: Review the file names used in the document itself and in related links; recommend lowercase letters separated by hyphens (e.g., `lowercase-with-hyphens.md`), and avoid spaces, underscores, or camelCase.
- **Link Validity**: Ensure all internal anchor links and external hyperlinks in the document are correctly formatted and logically reachable.
- **Image References**: Use relative paths; encode spaces in paths as `%20`.
- **Security and Redaction**: Check code blocks and configuration examples for real API keys, passwords, internal IPs, or private sensitive information; require placeholders such as `YOUR_API_KEY`.
- **References**:
  - **Single-Reference Markers**: Use bracketed numbered citations in the body text (e.g., `[1]`); the marker is usually placed before the punctuation.
  - **Multiple-Reference Markers**: When citing multiple references at the same point, combine them into a single bracket separated by commas (e.g., `[1, 2, 3]` or consecutive citations `[1-3]`). **Never** use separate brackets (incorrect examples: `[1][2][3]` or `[1], [2]`).
  - **Formatting Standards**: The reference list at the end of the document must be formatted professionally. **[Mandatory Cross-Skill Collaboration]** When the reference list is non-standard or needs supplementary metadata, you **must directly invoke the `reference-organizer` skill** (invoke `reference-organizer` via your skill invocation tool, or output the `/reference-organizer` command to prompt the user for collaborative handling). **Never attempt to fabricate citation formats yourself!** Only when the system explicitly reports that the skill does not exist may you fall back to the following basic standards:
    - **Blog/Web level (GB/T 7714-2015)**: `[No.] [Primary author]. [Title][EB/OL]. ([Update or modification date])[Cited date]. [Access path].`
    - **White Paper/Technical Report level (APA 7th)**: `[Publishing organization]. ([Year of publication]). *[Report title]*. [URL]`
    - **Paper level (IEEE)**:
      - Journal article: `[No.] [Author (Initial. Surname)], "[Article title]," *[Journal abbreviation]*, vol. [Vol.], no. [Issue], pp. [Page range], [Month abbreviation]. [Year].`
      - Conference paper: `[No.] [Author], "[Paper title]," in *Proc. [Conference abbreviation]*, [Conference city], [Conference country], [Year], pp. [Page range].`
      - Preprint: `[No.] [Author], "[Paper title]," arXiv preprint arXiv:[ID], [Year].`
  - **No Intro Needed**: The reference section is a special pure-list section and does **not** need an introductory paragraph; list the references directly.
  - **Consistency Check**: Verify that every citation number in the body text (e.g., `[1]`) has a corresponding entry in the end-of-document reference list, and conversely, that every listed reference is cited in the body text.
