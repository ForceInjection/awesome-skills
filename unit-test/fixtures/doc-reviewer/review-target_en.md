# 1. Demo Document Review Target

This section outlines the review objectives and scope of this document, aiming to demonstrate the output effects of the `doc-reviewer` skill's "Asset and Link Review" and "Format Review". The following contains several deliberately set boundaries and potential issues to facilitate the review tool in identifying and providing fix suggestions.

## 1.1 Link and Reference Examples

This subsection provides several examples of links and references for testing format and compliance.

- External link (missing protocol): [Example site](www.example.com)
- Normal external link (with protocol): [Example homepage](https://example.com)
- Internal anchor link: Please refer to [Format Details](#_format-details)

## 1.2 Image and Resource Examples

This subsection contains image and path references for testing path specifications and relative/absolute path constraints.

- Absolute path image: ![Absolute image]( /images/arch.png )
- Relative path image: ![Relative image](img/diagram.png)

## 1.3 Table and Typography Examples

This subsection demonstrates table and Chinese-English typography details, facilitating format review to identify issues.

| Item | Description |
| ---- | ---- |
| A    | Inline line break example: First line<br>Second line |
| B    | Chinese-English spacing example: Written in Python; supports vLLM, TGI and other frameworks. |

## 1.4 Sensitive Information and Placeholders

This subsection is used to test security and desensitization rules. The following are placeholder examples and do not contain real keys.

- Configuration example:

```env
# Example: Please use placeholders, do not fill in real keys
API_KEY=YOUR_API_KEY
SECRET=YOUR_SECRET
```

## _Format Details

This subsection is used for internal anchor jump testing.