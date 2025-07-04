def improve_medical_response(query, rag_response, rag_context): return rag_response or "Medical recall response"
def improve_medical_response_enhanced(query, response, medical_context): return improve_medical_response(query, response, medical_context)
