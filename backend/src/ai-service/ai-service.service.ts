import {
  BadGatewayException,
  BadRequestException,
  GatewayTimeoutException,
  Injectable,
  ServiceUnavailableException,
} from '@nestjs/common';
import type {
  BuscarContextoRequest,
  BuscarContextoResponse,
} from './ai-service.types.js';

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isResponse(value: unknown): value is BuscarContextoResponse {
  return (
    isRecord(value) &&
    typeof value.contexto === 'string' &&
    typeof value.distancia_minima === 'number' &&
    Number.isFinite(value.distancia_minima) &&
    Array.isArray(value.fontes) &&
    value.fontes.every(
      (fonte: unknown) =>
        isRecord(fonte) &&
        typeof fonte.arquivo === 'string' &&
        typeof fonte.pagina === 'number' &&
        Number.isInteger(fonte.pagina) &&
        fonte.pagina >= 1 &&
        typeof fonte.curso === 'string',
    )
  );
}

@Injectable()
export class AiService {
  async buscarContexto(
    consulta: BuscarContextoRequest,
  ): Promise<BuscarContextoResponse> {
    if (
      !consulta ||
      typeof consulta.pergunta !== 'string' ||
      !consulta.pergunta.trim() ||
      (consulta.curso !== undefined && typeof consulta.curso !== 'string') ||
      (consulta.perfil !== undefined && typeof consulta.perfil !== 'string') ||
      (consulta.top_k !== undefined &&
        (!Number.isSafeInteger(consulta.top_k) || consulta.top_k < 1))
    ) {
      throw new BadRequestException('Consulta de busca inválida.');
    }

    const endpoint = this.getEndpoint();
    const signal = AbortSignal.timeout(5000);
    let response: Response;
    try {
      response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          pergunta: consulta.pergunta,
          curso: consulta.curso ?? 'Geral',
          perfil: consulta.perfil ?? 'Todos',
          top_k: consulta.top_k ?? 3,
        }),
        signal,
        redirect: 'error',
      });
    } catch {
      if (signal.aborted) {
        throw new GatewayTimeoutException(
          'Tempo limite do serviço de busca excedido.',
        );
      }
      throw new ServiceUnavailableException('Serviço de busca indisponível.');
    }

    if (!response.ok) {
      await response.body?.cancel().catch(() => undefined);
      throw new BadGatewayException('Falha na resposta do serviço de busca.');
    }

    let result: unknown;
    try {
      result = await response.json();
    } catch {
      if (signal.aborted) {
        throw new GatewayTimeoutException(
          'Tempo limite do serviço de busca excedido.',
        );
      }
      throw new BadGatewayException('Resposta inválida do serviço de busca.');
    }
    if (!isResponse(result)) {
      throw new BadGatewayException('Resposta inválida do serviço de busca.');
    }
    return result;
  }

  private getEndpoint(): URL {
    try {
      const base = new URL(process.env.AI_SERVICE_URL ?? '');
      if (
        !['http:', 'https:'].includes(base.protocol) ||
        base.username ||
        base.password ||
        base.search ||
        base.hash ||
        base.pathname !== '/'
      ) {
        throw new Error('Invalid origin');
      }
      return new URL('/api/v1/buscar', base);
    } catch {
      throw new ServiceUnavailableException(
        'Serviço de busca não configurado.',
      );
    }
  }
}
