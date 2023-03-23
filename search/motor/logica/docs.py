def get_total_docs(index):
        total_docs = set()
        for term in index:
            for doc in index[term]:
                total_docs.add(doc)
        return total_docs