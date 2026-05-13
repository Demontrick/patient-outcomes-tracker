import httpx
import time
import asyncio

URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"

async def run_once(client, i):
    prompt = "Patient deteriorating. Give 3 recommendations."

    start = time.time()
    first = None

    async with client.stream("POST", URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": True
    }) as r:

        async for line in r.aiter_lines():
            if not line:
                continue

            import json
            data = json.loads(line)
            token = data.get("response", "")

            if token and first is None:
                first = time.time()

    return time.time() - start, (first - start if first else None)

async def main():
    async with httpx.AsyncClient(timeout=None) as client:
        totals = []
        first_tokens = []

        for i in range(5):
            total, first = await run_once(client, i)
            totals.append(total)
            first_tokens.append(first)
            print(f"Run {i+1}: first={first:.2f}s total={total:.2f}s")

        print("\n--- Summary ---")
        print("Avg first token:", sum(first_tokens)/len(first_tokens))
        print("Avg total:", sum(totals)/len(totals))
        print("Max total:", max(totals))

asyncio.run(main())