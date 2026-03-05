import requests
import json

BASE_URL = "http://localhost:8000"

print("🧪 Testing RAG Endpoints\n")

# Test 1: Health Check
print("1️⃣ Testing Health Check...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/rag/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 2: RAG Test Endpoint
print("2️⃣ Testing RAG with sample question...")
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/rag/test",
        json={"question": "What are the baggage rules?", "top_k": 3}
    )
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Question: {result.get('question')}")
    print(f"   Answer: {result.get('answer')}")
    print(f"   Sources: {result.get('metadata', {}).get('sources_consulted')}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 3: Simple Chat Endpoint
print("3️⃣ Testing Simple Chat Endpoint...")
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Tell me about flight delays"}
    )
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Reply: {result.get('reply')[:200]}...")
    print(f"   Sources: {result.get('metadata', {}).get('sources_consulted')}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

print("✅ Testing Complete!")
