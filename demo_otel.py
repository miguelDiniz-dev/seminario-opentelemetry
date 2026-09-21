import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# 1. Identifica o serviço
resource = Resource.create({"service.name": "sistema-pedidos-devops"})
provider = TracerProvider(resource=resource)

# 2. Configura envio para o Jaeger no ambiente do Codespaces
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("seminario.opentelemetry")

def processar_requisicao_completa():
    with tracer.start_as_current_span("POST /api/v1/pedidos") as main_span:
        main_span.set_attribute("http.status_code", 200)
        main_span.set_attribute("cliente.id", "usr_998822")
        
        # Etapa 1: Autenticação
        with tracer.start_as_current_span("autenticar_usuario") as span_auth:
            time.sleep(0.12)
            span_auth.set_attribute("auth.type", "Bearer JWT")
            
        # Etapa 2: Banco de Dados
        with tracer.start_as_current_span("SELECT * FROM estoque") as span_db:
            time.sleep(0.25)
            span_db.set_attribute("db.system", "postgresql")
            
        # Etapa 3: Gateway de Pagamento
        with tracer.start_as_current_span("processar_pagamento_credito") as span_pay:
            time.sleep(0.38)
            span_pay.set_attribute("payment.provider", "Stripe")
            span_pay.set_attribute("payment.status", "approved")

if __name__ == "__main__":
    print("Iniciando requisição simulada com OpenTelemetry...")
    processar_requisicao_completa()
    print("Aguardando envio ao Jaeger...")
    time.sleep(2)
    print("Pronto! Telemetria enviada com sucesso.")