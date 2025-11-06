"""Run the pipeline logic bypassing ZenML orchestration to avoid ZenML/SQL metadata errors.
This script creates/gets a user in MongoDB and runs the registered crawlers on the list of links.
"""
import os
from loguru import logger

# ensure USER_AGENT available
os.environ.setdefault("USER_AGENT", "my-agent/1.0")

from llm_engineering.domain.documents import UserDocument
import requests
from llm_engineering.application.crawlers.dispatcher import CrawlerDispatcher
from llm_engineering.domain.documents import ArticleDocument


def run_local(user_full_name: str, links: list[str]):
    # split name
    first_name, last_name = user_full_name.split(" ", 1) if " " in user_full_name else (user_full_name, "")

    logger.info(f"Getting or creating user: {user_full_name}")
    user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)
    logger.info(f"Using user id: {user.id} first: {user.first_name} last: {user.last_name}")

    # Use default dispatcher without registering site-specific crawlers
    # so the fallback CustomArticleCrawler (requests/html loader) is used
    # Simple fallback: fetch article HTML with requests and save minimal content
    for link in links:
        logger.info(f"Fetching {link}")
        try:
            # skip if already present
            if ArticleDocument.find(link=link) is not None:
                logger.info(f"Article already exists: {link}")
                continue

            resp = requests.get(link, headers={"User-Agent": os.environ.get("USER_AGENT", "my-agent/1.0")}, timeout=15)
            resp.raise_for_status()

            content = {
                "Title": None,
                "Subtitle": None,
                "Content": resp.text[:100000],
                "language": None,
            }

            parsed_platform = link.split("//")[-1].split("/")[0]

            instance = ArticleDocument(
                content=content,
                link=link,
                platform=parsed_platform,
                author_id=user.id,
                author_full_name=user.full_name,
            )
            instance.save()

            logger.info(f"Saved article: {link}")
        except Exception:
            logger.exception(f"Failed to fetch and save {link}")


if __name__ == "__main__":
    # Try to load the full article_links from run_pipeline.py using AST to avoid executing it
    import ast

    repo_root = os.path.dirname(__file__)
    run_pipeline_path = os.path.join(repo_root, "run_pipeline.py")
    links = []
    if os.path.exists(run_pipeline_path):
        try:
            with open(run_pipeline_path, "r", encoding="utf-8") as f:
                src = f.read()
            tree = ast.parse(src, filename=run_pipeline_path)
            # walk the AST to find article_links assignment anywhere (including inside if __name__ blocks)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if getattr(target, "id", None) == "article_links" and isinstance(node.value, (ast.List, ast.Tuple)):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                    links.append(elt.value)
        except Exception:
            links = []

    if not links:
        # fallback small set
        links = [
            "https://medium.com/decodingml/an-end-to-end-framework-for-production-ready-llm-systems-by-building-your-llm-twin-2cc6bb01141f",
            "https://medium.com/decodingml/a-real-time-retrieval-system-for-rag-on-social-media-data-9cc01d50a2a0",
            "https://medium.com/decodingml/sota-python-streaming-pipelines-for-fine-tuning-llms-and-rag-in-real-time-82eb07795b87",
            "https://decodingml.substack.com/p/dml-how-to-implement-a-streaming?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-why-and-what-do-you-need-a-streaming?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-unwrapping-the-3-pipeline-design?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-how-to-design-an-llm-system-for?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-synced-vector-dbs-a-guide-to?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-what-is-the-difference-between?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-7-steps-to-build-a-production?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-chain-of-thought-reasoning-write?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-build-and-serve-a-production?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-4-key-ideas-you-must-know-to?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-how-to-add-real-time-monitoring?r=1ttoeh",
            "https://decodingml.substack.com/p/dml-top-6-ml-platform-features-you?r=1ttoeh",
            "https://medium.com/@khayl/unlike-the-stomach-the-brain-doesnt-alert-you-when-it-s-empty-89430eb30860"
        ]

    user_name = "Paul Iusztin"
    logger.info(f"Loaded {len(links)} links to fetch")
    run_local(user_name, links)
