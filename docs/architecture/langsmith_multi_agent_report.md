
# REPORTE LANGSMITH - SISTEMA MULTI-AGENTE

## Información del Proyecto
- **Proyecto**: proyecto-final-agentes
- **URL LangSmith**: https://smith.langchain.com/projects/proyecto-final-agentes
- **Fecha**: 2025-10-17 12:00:20

## Resumen de Traces
- **Total de Traces**: 1

## Detalles por Trace

### Trace 1: multi_agent_query
- **Duración**: 3.05 segundos
- **Eventos**: 1
- **Metadatos**: {'query': '¿Qué me recomiendas para una cena romántica?', 'timestamp': '2025-10-17T12:00:17.632642', 'system': 'multi_agent_mozo_virtual'}
- **Resultado**: {'response': ' ¿Buscan un lugar con música en vivo, o prefieren un ambiente más íntimo y tranquilo? Con esta información, puedo generar un informe de recomendación más personalizado.', 'success': True, 'agents_used': ['investigator', 'generator']}

## Análisis de Rendimiento
- **Tiempo Total**: 3.05 segundos
- **Promedio por Trace**: 3.05 segundos
- **Traces más Largos**: [{'name': 'multi_agent_query', 'duration': 3.047559, 'events_count': 1, 'metadata': {'query': '¿Qué me recomiendas para una cena romántica?', 'timestamp': '2025-10-17T12:00:17.632642', 'system': 'multi_agent_mozo_virtual'}, 'result': {'response': ' ¿Buscan un lugar con música en vivo, o prefieren un ambiente más íntimo y tranquilo? Con esta información, puedo generar un informe de recomendación más personalizado.', 'success': True, 'agents_used': ['investigator', 'generator']}}]

## Observabilidad Implementada
- Tracing de LLM calls
- Tracing de tool calls
- Tracing de agent actions
- Metadatos de contexto
- Medición de rendimiento
- Reportes estructurados
