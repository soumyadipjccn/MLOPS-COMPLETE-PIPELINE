import json
from llm_engineering.domain.documents import UserDocument, ArticleDocument


def to_json(obj):
    try:
        return json.dumps(obj, default=str, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


def sample_documents(model, limit=10):
    docs = model.bulk_find()
    return docs[:limit]


def main():
    users = sample_documents(UserDocument, 10)
    articles = sample_documents(ArticleDocument, 10)

    print(f"users_count: {len(UserDocument.bulk_find())}")
    print(f"articles_count: {len(ArticleDocument.bulk_find())}\n")

    print("--- Sample users ---")
    for u in users:
        print(to_json(u.model_dump()))

    print("\n--- Sample articles ---")
    for a in articles:
        d = a.model_dump()
        # shorten content for display
        if isinstance(d.get('content'), dict) and d['content'].get('Content'):
            d['content']['Content'] = d['content']['Content'][:1000]
        print(to_json(d))

if __name__ == '__main__':
    main()
