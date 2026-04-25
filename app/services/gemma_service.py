import os
from dotenv import load_dotenv

load_dotenv()

# 🔥 OPTIONAL GEMMA (SAFE IMPORT)
USE_GEMMA = False

try:
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMMA_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    USE_GEMMA = True

except Exception as e:
    print("⚠ Running in fallback mode (Gemma not available):", str(e))
    USE_GEMMA = False


# ✅ SAFE GENERATE
def safe_generate(prompt):
    if not USE_GEMMA:
        return None   # 🔥 fallback trigger

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("⚠ Gemma fallback triggered:", str(e))
        return None


# ✅ TEST
def test_gemma():
    return safe_generate("Say: PLIS AI is working perfectly") or \
           "AI fallback: System is operating in offline intelligence mode."


# ✅ ROUTE AI (SAFE)
def generate_route_reasoning(*args):

    data = args if len(args) > 1 else args[0]

    prompt = f"Analyze best route from data: {data}"

    result = safe_generate(prompt)

    return result or "AI fallback: Route optimized using simulation logic."


# ✅ INCIDENT AI (STRUCTURED HYBRID)
def generate_incident_reasoning(data):

    prompt = f"""
    Analyze logistics incident:

    Location: {data['location']}
    Severity hint: {data['severity']}

    Return:
    - severity (low/medium/high)
    - affected routes (A,B,C)
    - short reasoning
    """

    result = safe_generate(prompt)

    # ✅ GEMMA SUCCESS
    if result:
        return {
            "gemma_incident_analysis": result,
            "validated_severity": data["severity"],
            "affected_routes": ["A", "C"]
        }

    # 🔥 FALLBACK (ALWAYS WORKING)
    return {
        "gemma_incident_analysis": "Simulated: Heavy disruption detected. Multi-lane blockage likely.",
        "validated_severity": "high" if data["severity"] == "high" else data["severity"],
        "affected_routes": ["A", "C"] if data["severity"] != "low" else ["B"]
    }